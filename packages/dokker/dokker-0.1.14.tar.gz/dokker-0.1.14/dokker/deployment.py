from pydantic import BaseModel, Field
from typing import Optional, List, Protocol, runtime_checkable
from koil.composition import KoiledModel
import asyncio
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from dokker.compose_spec import ComposeSpec
from dokker.project import Project
from typing import Union
from koil import unkoil
from dokker.cli import CLI
from dokker.loggers.void import VoidLogger
from .log_watcher import LogWatcher
import aiohttp
import certifi
from ssl import SSLContext
import ssl

ValidPath = Union[str, Path]


class HealthError(Exception):
    pass


class HealthCheck(BaseModel):
    url: str
    service: str
    max_retries: int = 3
    timeout: int = 10
    error_with_logs: bool = True
    headers: Optional[dict] = Field(default_factory=lambda: {"Content-Type": "application/json"})
    ssl_context: SSLContext = Field(
        default_factory=lambda: ssl.create_default_context(cafile=certifi.where()),
        description="SSL Context to use for the request",
    )

    async def acheck(self):
        async with aiohttp.ClientSession(
                headers=self.headers,
                connector=aiohttp.TCPConnector(ssl=self.ssl_context),
            ) as session:
                # get json from endpoint
                async with session.get(self.url) as resp:
                    assert resp.status == 200
                    return await resp.text()
                
    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True
                

@runtime_checkable
class Logger(Protocol):
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


class Deployment(KoiledModel):
    """A deployment is a set of services that are deployed together."""

    project: Project = Field(default_factory=Project)
    services: Optional[List[str]] = None

    health_checks: List[HealthCheck] = Field(default_factory=list)
    inspect_on_enter: bool = True
    pull_on_enter: bool = False
    up_on_enter: bool = True
    health_on_enter: bool = False
    down_on_exit: bool = False
    stop_on_exit: bool = True
    threadpool_workers: int = 3

    pull_logs: Optional[List[str]] = None
    up_logs: Optional[List[str]] = None
    stop_logs: Optional[List[str]] = None

    logger: Logger = Field(default_factory=VoidLogger)

    _spec: ComposeSpec
    _cli: CLI
    _threadpool: Optional[ThreadPoolExecutor] = None
    

    @property
    def spec(self) -> ComposeSpec:
        if self._spec is None:
            raise Exception(
                "Deployment not inspected. Call await deployment.ainspect() first."
            )
        return self._spec

    async def ainititialize(self) -> "CLI":
        self._cli = await self.project.ainititialize()
        return self._cli

    async def ainspect(self) -> ComposeSpec:
        if self._cli is None:
            await self.ainititialize()

        self._spec = await self._cli.ainspect_config()
        return self._spec

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


    async def acheck_healthz(self, check: HealthCheck, retry: int = 0):
        try:
            await check.acheck()
        except Exception as e:
            if retry < check.max_retries:
                await asyncio.sleep(check.timeout)
                await self.acheck_healthz(check, retry=retry + 1)
            else:
                if not check.error_with_logs:
                    raise HealthError(
                        f"Health check failed after {check.max_retries} retries. Logs are disabled."
                    ) from e

                logs = []
                
                async for std, i in  self._cli.astream_docker_logs(check.service):
                    logs.append(i)

                raise HealthError(
                    f"Health check failed after {check.max_retries} retries. Logs:\n"
                    + "\n".join(logs)
                ) from e

    async def await_for_healthz(
        self, timeout: int = 3, retry: int = 0, services: List[str] = None
    ):
        if services is None:
            services = [
                check.service for check in self.health_checks
            ]  # we check all services

        return await asyncio.gather(
            *[
                self.acheck_healthz(check)
                for check in self.health_checks
                if check.service in services
            ]
        )

    def logswatcher(self, service_name: str, **kwargs):
        return LogWatcher(cli_bearer=self, services=[service_name], tail=1, **kwargs)

    async def aup(self):
        logs = []
        async for type, log in self._cli.astream_up(stream_logs=True, detach=True):
            logs.append(log)
            self.logger.on_stop(log)

        return logs

    async def arestart(
        self, services: List[str] = None, await_health=True, await_health_timeout=3
    ):
        logs = []
        async for type, log in self._cli.astream_restart(services=services):
            logs.append(log)

        if await_health:
            await asyncio.sleep(await_health_timeout)
            await self.await_for_healthz(services=services)

        return logs

    def restart(
        self, services: List[str] = None, await_health=True, await_health_timeout=3
    ):
        return unkoil(
            self.arestart,
            services=services,
            await_health=await_health,
            await_health_timeout=await_health_timeout,
        )

    async def apull(self):
        logs = []
        async for type, log in self._cli.astream_pull(stream_logs=True, detach=True):
            logs.append(log)
            self.logger.on_pull(log)

        return logs

    async def adown(self):
        logs = []
        async for type, log in self._cli.astream_pull(stream_logs=True, detach=True):
            logs.append(log)
            self.logger.on_pull(log)

        return logs

    async def astop(self):
        logs = []
        async for type, log in self._cli.astream_stop():
            logs.append(log)
            self.logger.on_stop(log)

        return logs

    async def aget_cli(self):
        assert (
            self._cli is not None
        ), "Deployment not initialized. Call await deployment.ainitialize() first."
        return self._cli

    async def __aenter__(self):
        self._threadpool = ThreadPoolExecutor(max_workers=self.threadpool_workers)

        await self.ainititialize()

        if self.inspect_on_enter:
            await self.ainspect()

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
