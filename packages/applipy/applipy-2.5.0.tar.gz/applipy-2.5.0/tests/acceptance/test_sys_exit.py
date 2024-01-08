import time
from asyncio import get_event_loop, sleep, Future
from logging import Logger
from tempfile import NamedTemporaryFile
from typing import Type, Optional

from .common import ApplipyProcess
from applipy import (
    Module as Module_,
    AppHandle,
    LoggingModule,
    BindFunction,
    RegisterFunction,
    Config,
)


class App(AppHandle):
    def __init__(self, logger: Logger) -> None:
        self._logger = logger.getChild("test-app")
        self.future: Optional[Future[None]] = None

    async def on_init(self) -> None:
        self._logger.debug("on_init")

    async def on_start(self) -> None:
        self._logger.debug("on_start")
        self.future = get_event_loop().create_future()
        await self.future

    async def on_shutdown(self) -> None:
        self._logger.debug("on_shutdown")
        if self.future:
            self.future.set_result(None)


class AppExit(AppHandle):
    def __init__(self, logger: Logger, config: Config) -> None:
        self._logger = logger.getChild("test-app-exit")
        self._when_exit = config["test_sys_exit.when_exit"]
        self.future: Optional[Future[None]] = None

    async def on_init(self) -> None:
        self._logger.debug("on_init")
        if self._when_exit == "on_init":
            await sleep(1)
            exit(143)

    async def on_start(self) -> None:
        self._logger.debug("on_start")
        if self._when_exit == "on_start":
            await sleep(1)
            exit(148)
        self.future = get_event_loop().create_future()
        await self.future

    async def on_shutdown(self) -> None:
        self._logger.debug("on_shutdown")
        if self._when_exit == "on_shutdown":
            await sleep(1)
            exit(117)
        if self.future:
            self.future.set_result(None)


class Module(Module_):
    def configure(self, bind: BindFunction, register: RegisterFunction) -> None:
        register(App)
        register(AppExit)

    @classmethod
    def depends_on(cls) -> tuple[Type[Module_], ...]:
        return (LoggingModule,)


def test_applipy_immediate_exit_on_init() -> None:
    with NamedTemporaryFile("r") as f:
        with ApplipyProcess(
            "./tests/acceptance",
            "test_sys_exit",
            {"log_file": f.name, "when_exit": "on_init"},
        ) as p:
            time.sleep(3)

        assert p.returncode == 143
        f.seek(0)
        assert [
            s for s in f.readlines() if s.startswith("DEBUG:test_sys_exit.test-app:")
        ] == ["DEBUG:test_sys_exit.test-app:on_init\n"]
        f.seek(0)
        assert [
            s
            for s in f.readlines()
            if s.startswith("DEBUG:test_sys_exit.test-app-exit:")
        ] == ["DEBUG:test_sys_exit.test-app-exit:on_init\n"]


def test_applipy_immediate_exit_on_start() -> None:
    with NamedTemporaryFile("r") as f:
        with ApplipyProcess(
            "./tests/acceptance",
            "test_sys_exit",
            {"log_file": f.name, "when_exit": "on_start"},
        ) as p:
            time.sleep(3)

        assert p.returncode == 148
        f.seek(0)
        assert [
            s for s in f.readlines() if s.startswith("DEBUG:test_sys_exit.test-app:")
        ] == [
            "DEBUG:test_sys_exit.test-app:on_init\n",
            "DEBUG:test_sys_exit.test-app:on_start\n",
        ]
        f.seek(0)
        assert [
            s
            for s in f.readlines()
            if s.startswith("DEBUG:test_sys_exit.test-app-exit:")
        ] == [
            "DEBUG:test_sys_exit.test-app-exit:on_init\n",
            "DEBUG:test_sys_exit.test-app-exit:on_start\n",
        ]


def test_applipy_immediate_exit_on_shutdown() -> None:
    with NamedTemporaryFile("r") as f:
        with ApplipyProcess(
            "./tests/acceptance",
            "test_sys_exit",
            {"log_file": f.name, "when_exit": "on_shutdown"},
        ) as p:
            time.sleep(3)

        assert p.returncode == 117
        f.seek(0)
        assert [
            s for s in f.readlines() if s.startswith("DEBUG:test_sys_exit.test-app:")
        ] == [
            "DEBUG:test_sys_exit.test-app:on_init\n",
            "DEBUG:test_sys_exit.test-app:on_start\n",
            "DEBUG:test_sys_exit.test-app:on_shutdown\n",
        ]
        f.seek(0)
        assert [
            s
            for s in f.readlines()
            if s.startswith("DEBUG:test_sys_exit.test-app-exit:")
        ] == [
            "DEBUG:test_sys_exit.test-app-exit:on_init\n",
            "DEBUG:test_sys_exit.test-app-exit:on_start\n",
            "DEBUG:test_sys_exit.test-app-exit:on_shutdown\n",
        ]
