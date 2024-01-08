[![pipeline status](https://gitlab.com/applipy/applipy/badges/master/pipeline.svg)](https://gitlab.com/applipy/applipy/-/pipelines?scope=branches&ref=master)
[![coverage report](https://gitlab.com/applipy/applipy/badges/master/coverage.svg)](https://gitlab.com/applipy/applipy/-/graphs/master/charts)
[![PyPI Status](https://img.shields.io/pypi/status/applipy.svg)](https://pypi.org/project/applipy/)
[![PyPI Version](https://img.shields.io/pypi/v/applipy.svg)](https://pypi.org/project/applipy/)
[![PyPI Python](https://img.shields.io/pypi/pyversions/applipy.svg)](https://pypi.org/project/applipy/)
[![PyPI License](https://img.shields.io/pypi/l/applipy.svg)](https://pypi.org/project/applipy/)
[![PyPI Format](https://img.shields.io/pypi/format/applipy.svg)](https://pypi.org/project/applipy/)

# Applipy

A library for building modular applications.

    pip install applipy

Applipy lets you:
 - implement self-contained or interdependant [`Module`s](#modules) that you
   can tell applipy to load for the application through the config file
 - implement [`AppHandle`s](#apphandle): instances that implement application
   lifecycle methods
 - modules can register multiple `AppHandle`s that will be run concurrently
 - load your application from a configuration file
 - applipy will gracefully manage the lifecycle of your application
 - define [protocol
   handlers](https://gitlab.com/applipy/applipy/-/blob/master/docs/config.md#config-protocols)
   for a given URI scheme in configuration values. With these you can implement
   [secrets](https://gitlab.com/applipy/applipy/-/blob/master/docs/config.md#applipyconfigprotocolsdockersecrets)
   that can be accessed by the application through the configuration.

## Usage

An application can be defined by using a JSON (or YAML, if `pyyaml` is
installed).

```yaml
# dev.yaml
app:
  name: demo
  modules:
  - applipy_http.HttpModule
  - applipy_prometheus.PrometheusModule

logging.level: DEBUG

http.servers:
- host: 0.0.0.0
  port: 8080
```

Save a file `dev.yaml` with the contents in the snipet above and run the
following commands:
```
$ pip install pyyaml applipy applipy_http applipy_prometheus
$ applipy
```

The configuration file above defines an application named `demo` that installs
the applipy web module and the Prometheus module.

You can try it by going to [http://localhost:8080](http://localhost:8080). To
see some metrics you have to call at least twice on the
http://0.0.0.0:8080/metrics endpoint.

Applipy will search for a configuration file named
`${APPLIPY_CONFIG_PATH}/${APPLIPY_ENV}.json` (and
`${APPLIPY_CONFIG_PATH}/${APPLIPY_ENV}.yaml`, if `pyyaml` is installed). The
default values are: `APPLIPY_ENV=dev` and `APPLIPY_CONFIG_PATH=.`.

Another option is to indicate the file directly, using `applipy -f ./path/to/file.yaml`.

## AppHandle

AppHandle is the interface through wich applipy manages the lifecycle of the
application. An AppHandle implementation looks like this:

```python
# demo_app.py
from asyncio import get_event_loop
from logging import Logger

from applipy import AppHandle


class MyDemoApp(AppHandle):

    def __init__(self, logger: Logger, name: str):
        self.logger = logger.getChild(name)

    async def on_init(self):
        self.logger.info('initialize resources')
        self.future = get_event_loop().create_future()

    async def on_start(self):
        self.logger.info('run long lived application here')
        await self.future

    async def on_shutdown(self):
        self.logger.info('close and release resources')
        self.future.set_result(None)
```

As you can see above there is three methods exposed by AppHandles that let
applipy run your application.

Applipy is capable of running multiple AppHandles concurrently,
taking advantage of async in python.

The lifecycle of an application follow the following diagram:

```
  Application.start()
           │
           ▼
  AppHandle.on_init()
           │
           ▼
  AppHandle.on_start()        applipy cli
           │                SIGINT   SIGTERM   [Your own stopping mechanism]
           ▼                   └────────┴───────┬───────────┘
start_long_running_task()                       ▼
           │                            Application.stop()
           ▼                                    │
 AppHandle.on_shutdown()◄───────────────────────┘
           │
           ▼
  wait(shutdown_timeout)
           │
           ▼
   cancel_all_tasks()
```

> *shutdown_timeout* can be set in the app configuration using the key
> `app.shutdown_timeout_seconds`. Defaults to 1 second.
>
> It is expected that `AppHandle.on_shutdown()` will be used to indicate any
> long running tasks to stop and cleanup, and do any required cleanup itself.

Generally, AppHandle implementations are added to the applipy application by
including the modules they are part of and registering the AppHandle in the
module `configure()` function.

## Modules

In applipy, modules are the building blocks of an application. They allow to
bind instances/classes/providers to types by exposing the an
[`applipy_inject.Injector`](https://gitlab.com/applipy/applipy_inject)'s
`bind()` function, register application handles by exposing the Application's
`register()` function and define dependencies across modules.

An example of a module implementation looks like this:
```python
# mymodule.py

from applipy import Config, Module, LoggingModule
from demo_app import MyDemoApp


class MyModule(Module):

    def __init__(self, config: Config):
        self._config = config

    def configure(self, bind, register):
        bind(str, 'ModuleDemo')
        register(MyDemoApp)

    @classmethod
    def depends_on(cls):
        return (LoggingModule,)
```

The way you add modules to an application is through the configuration file by
defining a list of fully qualified names of Module implementations with
the key `app.modules`:

```yaml
app:
  modules:
    - applipy_http.HttpModule
    - applipy_prometheus.PrometheusModule
    - mymodule.MyModule
```

Modules can only receive one parameter in their constructor and it is a
`Config` instance, as shown in the code above. If your module does not need
access to the configuration, you can just not implement a `__init__` or have it
not have arguments (other than `self`).

The `configure()` method is run by the applipy `Application` when it is started
and its purpose is to allow for binding types and registering application
handles. Check the extended `Module` documentation in
[`/docs/module.md`](https://gitlab.com/applipy/applipy/-/blob/master/docs/module.md).

Finally, the `depends_on()` class method returns a tuple of the module types the
module depends on. In the example above, because the application handle
registered by the module requires a `logging.Logger`, the module declares a dependency
with the `LoggingModule` because we know that it binds the `logging.Logger` type.

## More

For a deeper dive on the features and details feel free to check the
[`/docs`](https://gitlab.com/applipy/applipy/-/blob/master/docs/README.md)
subdirectory and the code itself!
