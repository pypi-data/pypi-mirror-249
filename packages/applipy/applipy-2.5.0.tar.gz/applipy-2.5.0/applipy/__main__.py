import asyncio
import json
import os
import signal
import sys
from logging import ERROR, INFO
from pydoc import locate
from typing import (
    Any,
    Dict,
    cast,
)

from applipy_inject import Injector

from applipy import Application, Config
from applipy.application.application import (
    FallbackLogger,
    ModuleManager,
)
from applipy.application.module import Module


try:
    import yaml

    yaml_defined = True
except ImportError:
    yaml_defined = False


def load_modules_from_config(injector: Injector, config: Config) -> ModuleManager:
    module_manager = ModuleManager(injector, config)
    module_names = config.get("app.modules")
    if module_names:
        for module, name in ((locate(name), name) for name in module_names):
            if module and isinstance(module, type) and issubclass(module, Module):
                module_manager.install(module)
            else:
                module_manager.log(ERROR, f"Could not load module `{name}`")
                raise ImportError(name)
    return module_manager


def _is_file(path: str) -> bool:
    return os.path.isfile(path) or (os.path.exists(path) and not os.path.isdir(path))


def load_config_from_json(config_file: str) -> Dict[str, Any]:
    if _is_file(config_file):
        with open(config_file, "r") as f:
            config = cast(Dict[str, Any], json.load(f))
    else:
        config = {}
    return config


def load_config_from_yaml(config_file: str) -> Dict[str, Any]:
    is_file = _is_file(config_file)
    if yaml_defined and is_file:
        with open(config_file, "r") as f:
            config = cast(Dict[str, Any], yaml.load(f, Loader=yaml.Loader))
    else:
        if is_file:
            print(f"[WARN] Found `{config_file}` but no yaml module installed")
        config = {}
    return config


def load_raw_config(config_path: str, env: str) -> Dict[str, Any]:
    return {
        **load_config_from_yaml(os.path.join(config_path, f"{env.lower()}.yaml")),
        **load_config_from_yaml(os.path.join(config_path, f"{env.lower()}.yml")),
        **load_config_from_json(os.path.join(config_path, f"{env.lower()}.json")),
    }


def build_config(config_raw: Dict[str, Any]) -> Config:
    config = Config(config_raw)

    provider_names = config.get("config.protocols")
    if provider_names:
        for provider, name in ((locate(name), name) for name in provider_names):
            if provider and callable(provider):
                print(f"[INFO] Adding configuration provider `{name}`")
                config.addProtocol(provider())
            else:
                print(f"[ERROR] Could not load configuration provider `{name}`")
                raise ImportError(name)

    return config


def start(config: Config) -> None:
    injector = Injector()
    fallback_logger = FallbackLogger(injector, config)
    module_manager = load_modules_from_config(injector, config)
    shutdown_timeout_seconds = config.get("app.shutdown_timeout_seconds", 1)
    loop = asyncio.new_event_loop()
    app = Application(
        config,
        shutdown_timeout_seconds=shutdown_timeout_seconds,
        injector=injector,
        module_manager=module_manager,
        loop=loop,
    )

    def _sigterm_handler() -> None:
        fallback_logger.log(INFO, "Received SIGTERM. Shutting down.")
        app.stop()

    loop.add_signal_handler(signal.SIGTERM, _sigterm_handler)

    def _sigint_handler() -> None:
        fallback_logger.log(INFO, "Received SIGINT. Shutting down.")
        app.stop()

    loop.add_signal_handler(signal.SIGINT, _sigint_handler)

    app.run()


def main(config_path: str, env: str) -> None:
    start(build_config(load_raw_config(config_path, env)))


def main_cmd(config_file: str) -> None:
    if config_file.endswith(".json"):
        config = load_config_from_json(config_file)
    else:
        config = load_config_from_yaml(config_file)
    start(build_config(config))


def entrypoint() -> None:
    config_file = None
    try:
        idx = sys.argv.index("-f")
        config_file = sys.argv[idx + 1]
    except IndexError:
        config_file = "/dev/stdin"
    except ValueError:
        ...

    if config_file:
        main_cmd(config_file)
    else:
        main(
            os.environ.get("APPLIPY_CONFIG_PATH", os.path.curdir),
            os.environ.get("APPLIPY_ENV", "DEV"),
        )


if __name__ == "__main__":
    entrypoint()
