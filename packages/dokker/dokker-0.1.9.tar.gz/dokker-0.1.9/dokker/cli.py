from typing import Optional, List, Union, Protocol, runtime_checkable
from pydantic import BaseModel, Field
from pydantic.types import DirectoryPath, FilePath
from koil.composition import KoiledModel
from pathlib import Path
import asyncio
from datetime import timedelta
from typing import Union, Callable, Dict, Literal
from .compose_spec import ComposeSpec
import json

ValidPath = Union[str, Path]


@runtime_checkable
class CLIBearer(Protocol):
    async def aget_cli(self) -> "CLI":
        ...


class CLI(KoiledModel):
    """A CLI object that represents the docker-compose CLI.

    This is a pydantic model that can be used to build the docker-compose CLI
    command. It also contains methods for running the CLI command
    asynchronously.

    """

    config: Optional[ValidPath] = None
    context: Optional[str] = None
    debug: Optional[bool] = None
    host: Optional[str] = None
    log_level: Optional[str] = None
    tls: Optional[bool] = None
    tlscacert: Optional[ValidPath] = None
    tlscert: Optional[ValidPath] = None
    tlskey: Optional[ValidPath] = None
    tlsverify: Optional[bool] = None
    compose_files: List[ValidPath] = Field(
        default_factory=lambda: ["docker-compose.yml"]
    )
    compose_profiles: List[ValidPath] = Field(default_factory=list)
    compose_env_file: Optional[ValidPath] = Field(default=".env")
    compose_project_name: Optional[str] = None
    compose_project_directory: Optional[ValidPath] = None
    compose_compatibility: Optional[bool] = None
    client_call: List[str] = Field(default_factory=lambda: ["docker", "compose"])

    @property
    def docker_cmd(self) -> list[str]:
        """Builds the docker command. This is the base prepended
        command that will be run by the CLI.
        """
        result = self.client_call

        if self.config is not None:
            result += ["--config", self.config]

        if self.context is not None:
            result += ["--context", self.context]

        if self.debug:
            result.append("--debug")

        if self.host is not None:
            result += ["--host", self.host]

        if self.log_level is not None:
            result += ["--log-level", self.log_level]

        if self.tls:
            result.append("--tls")

        if self.tlscacert is not None:
            result += ["--tlscacert", self.tlscacert]

        if self.tlscert is not None:
            result += ["--tlscert", self.tlscert]

        if self.tlskey is not None:
            result += ["--tlskey", self.tlskey]

        if self.tlsverify:
            result.append("--tlsverify")

        return result

    async def arun(command: str):
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await proc.communicate()

        return stdout.decode("utf-8"), stderr.decode("utf-8")

    async def astream_docker_logs(
        self,
        tail: Optional[str] = None,
        follow: bool = False,
        no_log_prefix: bool = False,
        timestamps: bool = False,
        since: Optional[str] = None,
        until: Optional[str] = None,
        services: Union[str, List[str]] = [],
    ):
        full_cmd = self.docker_cmd + ["logs", "--no-color"]
        if tail is not None:
            full_cmd += ["--tail", tail]
        if follow:
            full_cmd.append("--follow")
        if no_log_prefix:
            full_cmd.append("--no-log-prefix")
        if timestamps:
            full_cmd.append("--timestamps")
        if since is not None:
            full_cmd += ["--since", since]
        if until is not None:
            full_cmd += ["--until", until]

        if services:
            if isinstance(services, str):
                services = [services]
            full_cmd += services

        async for line in self.astream_command(full_cmd):
            yield line

    async def _astread_stream(
        self,
        stream: asyncio.StreamReader,
        queue: asyncio.Queue,
        name: str,
    ):
        async for line in stream:
            await queue.put((name, line.decode("utf-8").strip()))

        await queue.put(None)

    async def astream_command(self, command: List[str]):
        # Create the subprocess using asyncio's subprocess

        full_cmd = " ".join(map(str, command))

        proc = await asyncio.create_subprocess_shell(
            full_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        queue = asyncio.Queue()
        # Create and start tasks for reading each stream

        try:
            readers = [
                asyncio.create_task(self._astread_stream(proc.stdout, queue, "STDOUT")),
                asyncio.create_task(self._astread_stream(proc.stderr, queue, "STDERR")),
            ]

            # Track the number of readers that are finished
            finished_readers = 0
            while finished_readers < len(readers):
                line = await queue.get()
                if line is None:
                    finished_readers += 1  # One reader has finished
                    continue
                yield line

            # Cleanup: cancel any remaining reader tasks
            for reader in readers:
                reader.cancel()
                try:
                    await reader
                except asyncio.CancelledError:
                    pass

        except asyncio.CancelledError:
            # Handle cancellation request
            proc.kill()
            await proc.wait()  # Wait for the subprocess to exit after receiving SIGINT

            # Cleanup: cancel any remaining reader tasks
            for reader in readers:
                reader.cancel()
                try:
                    await reader
                except asyncio.CancelledError:
                    pass

            raise

        except Exception as e:
            raise e

    async def astream_pull(
        self,
        services: Union[List[str], str, None] = None,
        ignore_pull_failures: bool = False,
        include_deps: bool = False,
        quiet: bool = False,
    ):
        full_cmd = self.docker_cmd + ["pull"]
        if ignore_pull_failures:
            full_cmd.append("--ignore-pull-failures")
        if include_deps:
            full_cmd.append("--include-deps")
        if quiet:
            full_cmd.append("--quiet")

        if services:
            if isinstance(services, str):
                services = [services]
            full_cmd += services

        async for line in self.astream_command(full_cmd):
            yield line

    async def astream_stop(
        self,
        services: Union[str, List[str], None] = None,
        timeout: Union[int, timedelta, None] = None,
        stream_logs: bool = False,
    ):
        full_cmd = self.docker_cmd + ["stop"]
        if timeout is not None:
            if isinstance(timeout, timedelta):
                timeout = int(timeout.total_seconds())

            full_cmd.append(f"--timeout {timeout}")

        if services:
            if isinstance(services, str):
                services = [services]
            full_cmd += services

        async for line in self.astream_command(full_cmd):
            yield line

    async def astream_up(
        self,
        services: Union[List[str], str, None] = None,
        build: bool = False,
        detach: bool = False,
        abort_on_container_exit: bool = False,
        scales: Dict[str, int] = {},
        attach_dependencies: bool = False,
        force_recreate: bool = False,
        no_recreate: bool = False,
        no_build: bool = False,
        remove_orphans: bool = False,
        renew_anon_volumes: bool = False,
        no_color: bool = False,
        no_log_prefix: bool = False,
        no_start: bool = False,
        quiet: bool = False,
        wait: bool = False,
        no_attach_services: Union[List[str], str, None] = None,
        pull: Literal["always", "missing", "never", None] = None,
        stream_logs: bool = False,
    ):
        if quiet and stream_logs:
            raise ValueError(
                "It's not possible to have stream_logs=True and quiet=True at the same time. "
                "Only one can be activated at a time."
            )
        full_cmd = self.docker_cmd + ["up"]
        if build:
            full_cmd.append("--build")
        if detach:
            full_cmd.append("--detach")
        if abort_on_container_exit:
            full_cmd.append("--abort-on-container-exit")
        for service, scale in scales.items():
            full_cmd.append(f"--scale {service}={scale}")
        if attach_dependencies:
            full_cmd.append("--attach-dependencies")
        if force_recreate:
            full_cmd.append("--force-recreate")
        if no_recreate:
            full_cmd.append("--no-recreate")
        if no_build:
            full_cmd.append("--no-build")
        if remove_orphans:
            full_cmd.append("--remove-orphans")
        if renew_anon_volumes:
            full_cmd.append("--renew-anon-volumes")
        if no_color:
            full_cmd.append("--no-color")
        if no_log_prefix:
            full_cmd.append("--no-log-prefix")
        if no_start:
            full_cmd.append("--no-start")
        if quiet:
            full_cmd.append("--quiet")
        if wait:
            full_cmd.append("--wait")
        if no_attach_services is not None:
            if isinstance(no_attach_services, str):
                no_attach_services = [no_attach_services]
            for service in no_attach_services:
                full_cmd.append(f"--no-attach {service}")
        if pull is not None:
            full_cmd.append(f"--pull {pull}")

        if services:
            if isinstance(services, str):
                services = [services]
            full_cmd += services

        async for line in self.astream_command(full_cmd):
            yield line

    async def ainspect_config(self) -> ComposeSpec:
        """Returns the configuration of the compose stack for further inspection.

        For example
        ```python
        from python_on_whales import docker
        project_config = docker.compose.config()
        print(project_config.services["my_first_service"].image)
        "redis"
        ```

        Parameters:
            return_json: If `False`, a `ComposeConfig` object will be returned, and you
                'll be able to take advantage of your IDE autocompletion. If you want the
                full json output, you may use `return_json`. In this case, you'll get
                lists and dicts corresponding to the json response, unmodified.
                It may be useful if you just want to print the config or want to access
                a field that was not in the `ComposeConfig` class.

        # Returns
            A `ComposeConfig` object if `return_json` is `False`, and a `dict` otherwise.
        """
        full_cmd = self.docker_cmd + ["config", "--format", "json"]

        lines = []

        async for x, line in self.astream_command(full_cmd):
            lines.append(line)

        result = "\n".join(lines)

        try:
            return ComposeSpec(**json.loads(result))
        except Exception as e:
            raise Exception(
                f"Could not inspect! Error while parsing the json: {result}"
            ) from e
