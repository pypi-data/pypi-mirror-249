from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List, Protocol, runtime_checkable
from httpx import AsyncClient
import time
from koil.composition import KoiledModel
import asyncio
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from dokker.compose_spec import ComposeConfig
from dokker.project import Project
from typing import Union, Callable
from koil import unkoil
from dokker.cli import CLI
import traceback

try:
    from rich import panel

    def format_log_watcher_message(watcher: "LogWatcher", exc_val, rich=True):
        extra_info = map(
            lambda x: x[1] if x[0] == "STDERR" or watcher.capture_stdout else "",
            watcher.collected_logs,
        )
        # Ensure compatibility with different exception types

        extra_info = "\n".join(extra_info)

        if not rich:
            return f"{str(exc_val)}\n\nDuring the execution Logwatcher captured these logs from the services {watcher.services}:\n{extra_info}"
        else:
            return f"{str(exc_val)}\n\nDuring the execution Logwatcher captured these logs from the services {watcher.services}:\n{extra_info}"

except ImportError:

    def format_log_watcher_message(watcher: "LogWatcher", exc_val, extra_info):
        extra_info = map(
            lambda x: x[1] if x[0] == "STDERR" or watcher.capture_stdout else "",
            watcher.collected_logs,
        )
        # Ensure compatibility with different exception types

        extra_info = "\n".join(extra_info)
        return f"{str(exc_val)}\n\nDuring the execution Logwatcher captured these logs from the services {watcher.services}:\n{extra_info}"


ValidPath = Union[str, Path]


class HealthError(Exception):
    pass


class HealthCheck(BaseModel):
    url: str
    service: str
    max_retries: int = 3
    timeout: int = 10
    error_with_logs: bool = True


@runtime_checkable
class LogForward(Protocol):
    def on_pull(self, log: str):
        ...

    def on_up(self, log: str):
        ...

    def on_stop(self, log: str):
        ...

    def on_logs(self, log: str):
        ...

    def on_down(self, log: str):
        ...


class PrintLogger(LogForward):
    def on_pull(self, log: str):
        print(log)

    def on_up(self, log: str):
        print(log)

    def on_stop(self, log: str):
        print(log)

    def on_logs(self, log: str):
        print(log)

    def on_down(self, log: str):
        print(log)


class Logger(BaseModel):
    logger: logging.Logger = Field(default_factory=lambda: logging.getLogger(__name__))
    log_level: int = logging.INFO

    def on_pull(self, log: str):
        self.logger.log(self.log_level, log)

    def on_up(self, log: str):
        self.logger.log(self.log_level, log)

    def on_stop(self, log: str):
        self.logger.log(self.log_level, log)

    def on_logs(self, log: str):
        self.logger.log(self.log_level, log)

    def on_down(self, log: str):
        self.logger.log(self.log_level, log)

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


class LogWatcher(KoiledModel):
    setup: "Setup"
    tail: Optional[str] = None
    follow: bool = True
    no_log_prefix: bool = False
    timestamps: bool = False
    since: Optional[str] = None
    until: Optional[str] = None
    stream: bool = True
    services: Union[str, List[str]] = ([],)
    wait_for_first_log: bool = True
    wait_for_logs: bool = False
    wait_for_logs_timeout: int = 10
    collected_logs: List[str] = []
    log_function: Optional[Callable] = None
    append_to_traceback: bool = True
    capture_stdout: bool = True
    rich_traceback: bool = True

    _watch_task: Optional[asyncio.Task] = None
    _just_one_log: Optional[asyncio.Future] = None

    async def aon_logs(self, log: str):
        if self.log_function:
            if asyncio.iscoroutinefunction(self.log_function):
                await self.log_function(log)
            else:
                self.log_function(log)

    async def awatch_logs(self):
        async for log in self.setup._cli.astream_docker_logs(
            tail=self.tail,
            follow=self.follow,
            no_log_prefix=self.no_log_prefix,
            timestamps=self.timestamps,
            since=self.since,
            until=self.until,
            services=self.services,
        ):
            if self._just_one_log is not None and not self._just_one_log.done():
                self._just_one_log.set_result(True)
            await self.aon_logs(log)
            self.collected_logs.append(log)

    def on_watch_task_done(self, task: asyncio.Task):
        if task.cancelled():
            return
        if task.exception():
            raise task.exception()
        if task.done():
            return

    async def __aenter__(self):
        self.collected_logs = []
        self._just_one_log = asyncio.Future()
        self._watch_task = asyncio.create_task(self.awatch_logs())
        self._watch_task.add_done_callback(self.on_watch_task_done)

        if self.wait_for_first_log:
            await self._just_one_log

        self._just_one_log = asyncio.Future()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and self.append_to_traceback:
            new_message = format_log_watcher_message(
                self, exc_val, rich=self.rich_traceback
            )
            try:
                new_exc = exc_type(new_message)
            except:
                new_exc = Exception(new_message)

            raise new_exc.with_traceback(exc_tb) from exc_val

        if self.wait_for_logs:
            if self._just_one_log is not None:
                await asyncio.wait_for(self._just_one_log, self.wait_for_logs_timeout)

        if self._watch_task is not None:
            self._watch_task.cancel()

            try:
                await self._watch_task
            except asyncio.CancelledError:
                pass

        self._watch_task = None

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


class Setup(KoiledModel):
    project: Project = Field(default_factory=Project)
    services: Optional[List[str]] = None

    health_checks: Optional[List[HealthCheck]] = Field(default_factory=list)
    pull_on_enter: bool = False
    up_on_enter: bool = True
    health_on_enter: bool = False
    down_on_exit: bool = False
    stop_on_exit: bool = True
    threadpool_workers: int = 3

    pull_logs: Optional[List[str]] = None
    up_logs: Optional[List[str]] = None
    stop_logs: Optional[List[str]] = None

    logger: LogForward = Field(default_factory=Logger)

    _spec: ComposeConfig
    _cli: CLI
    _threadpool: Optional[ThreadPoolExecutor] = None

    @property
    def spec(self) -> ComposeConfig:
        if self._spec is None:
            raise Exception(
                "Setup not initialized. Call await setup.ainitialize() first."
            )
        return self._spec

    async def ainititialize(self) -> None:
        self._cli = await self.project.ainititialize()
        self._spec = await self.project.ainit_spec()

    def add_health_check(
        self,
        url: str = None,
        service: str = None,
        max_retries: int = 3,
        timeout: int = 10,
        error_with_logs: bool = True,
        check: HealthCheck = None,
    ) -> "HealthCheck":
        if check is None:
            check = HealthCheck(
                url=url,
                service=service,
                max_retries=max_retries,
                timeout=timeout,
                error_with_logs=error_with_logs,
            )

        self.health_checks.append(check)
        return check

    async def arequest(
        self, service_name: str, private_port: int = None, path: str = "/"
    ):
        async with AsyncClient() as client:
            try:
                response = await client.get(f"http://127.0.0.1:{private_port}{path}")
                assert response.status_code == 200
                return response
            except Exception as e:
                raise AssertionError(f"Health check failed: {e}")

    def request(self, service_name: str, private_port: int = None, path: str = ""):
        return unkoil(self.arequest, service_name, private_port=private_port, path=path)

    async def acheck_healthz(self, check: HealthCheck, retry: int = 0):
        try:
            async with AsyncClient() as client:
                try:
                    response = await client.get(check.url)
                    assert response.status_code == 200
                    return response
                except Exception as e:
                    raise AssertionError(f"Health check failed: {e}")
        except Exception as e:
            if retry < check.max_retries:
                await asyncio.sleep(check.timeout)
                await self.acheck_healthz(check, retry=retry + 1)
            else:
                if not check.error_with_logs:
                    raise HealthError(
                        f"Health check failed after {check.max_retries} retries. Logs are disabled."
                    ) from e

                logs = await self.afetch_service_logs(check.service)

                raise HealthError(
                    f"Health check failed after {check.max_retries} retries. Logs:\n"
                    + "".join(logs)
                ) from e

    async def await_for_healthz(self, timeout: int = 3, retry: int = 0):
        return await asyncio.gather(
            *[self.acheck_healthz(check) for check in self.health_checks]
        )

    def logswatcher(self, service_name: str, **kwargs):
        return LogWatcher(setup=self, services=[service_name], tail=1, **kwargs)

    async def ainititialize(self):
        self._cli = await self.project.ainititialize()
        self._spec = await self._cli.ainspect_config()

    async def aup(self):
        logs = []
        async for type, log in self._cli.astream_up(stream_logs=True, detach=True):
            logs.append(log)
            print(log)
            self.logger.on_stop(log)

        return logs

    async def apull(self):
        logs = []
        async for type, log in self._cli.astream_pull(stream_logs=True, detach=True):
            logs.append(log)
            print(log)
            self.logger.on_pull(log)

        return logs

    async def adown(self):
        logs = []
        async for type, log in self._cli.astream_pull(stream_logs=True, detach=True):
            logs.append(log)
            print(log)
            self.logger.on_pull(log)

        return logs

    async def astop(self):
        logs = []
        async for type, log in self._cli.astream_stop():
            logs.append(log)
            print(log)
            self.logger.on_stop(log)

        return logs

    async def __aenter__(self):
        self._threadpool = ThreadPoolExecutor(max_workers=self.threadpool_workers)

        await self.ainititialize()
        if self.pull_on_enter:
            await self.project.abefore_pull()
            await self.apull()

        if self.up_on_enter:
            await self.project.abefore_up()
            await self.aup()

        if self.health_on_enter:
            if self.health_checks:
                await self.await_for_healthz()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.stop_on_exit:
            await self.project.abefore_stop()
            await self.astop()

        if self.down_on_exit:
            await self.project.abefore_down()
            await self.adown()
        self._cli = None

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


Setup.update_forward_refs()
LogWatcher.update_forward_refs()
