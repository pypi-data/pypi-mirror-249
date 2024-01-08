from asyncio import get_event_loop, Future
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


class Module(Module_):
    def configure(self, bind: BindFunction, register: RegisterFunction) -> None:
        register(App)

    @classmethod
    def depends_on(cls) -> tuple[Type[Module_], ...]:
        return (LoggingModule,)


def test_applipy_timeout_on_shutdown() -> None:
    with NamedTemporaryFile("r") as f:
        with ApplipyProcess(
            "./tests/acceptance", "test_timeout", {"log_file": f.name}
        ) as p:
            ...
        assert p.returncode == 0
        f.seek(0)
        print("".join(f.readlines()))
        f.seek(0)
        assert [
            s for s in f.readlines() if s.startswith("DEBUG:test_timeout.test-app:")
        ] == [
            "DEBUG:test_timeout.test-app:on_init\n",
            "DEBUG:test_timeout.test-app:on_start\n",
            "DEBUG:test_timeout.test-app:on_shutdown\n",
        ]
