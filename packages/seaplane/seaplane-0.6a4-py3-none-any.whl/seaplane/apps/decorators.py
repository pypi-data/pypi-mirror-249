import functools
from typing import Any, Callable, Generator, Iterable, List, Optional, Protocol, cast
from warnings import warn
from contextlib import contextmanager

from seaplane.logs import log
from seaplane.pipes import App, Task, EdgeFrom


class LegacyAppsCompat:
    """
    a LEGACY application. New applications should use the new app toolkit
    """

    def __init__(
        self,
        func: Callable[[Any], Any],  # user code that assembles the task DAG.
        type: str,  # "stream" or "API"
        parameters: List[str],  # when type == "stream", [STREAM_NAME]
        id: str,
    ) -> None:
        self.id = id
        self.func = func
        self.real_app = App(self.id)

        if type != "API" or len(parameters) > 0:
            raise RuntimeError(
                "'stream' type apps are no longer supported."
                " To listen to arbitrary streams, use the new app construction tools"
            )

    def __call__(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError(
            "Don't call your legacy app directly. Instead, call seaplane.apps.start()"
        )

    def assemble(self) -> None:
        """
        Executes the app function, which in turn calls task.wire_up to assemble
        task sources.
        """
        with legacy_context.using_current_app(self):
            last = self.func(self.real_app.input())

        if last is not None:
            self.real_app.edge(last, self.real_app.output())


class LegacyTaskCompat:
    """
    Tasks are weird use / mention hybrids: in a deployment
    context, they are a map of Seaplane carrier flows and
    the connections between them. In an execution context
    on the Seaplane platform, they're containers for executable
    code that get the results of endpoints or tasks as input and can
    emit good things to their downstream flows and endpoints.
    """

    def __init__(
        self,
        func: Callable[[Any], Any],
        id: str,
        ack_wait: int = 8,
        replicas: int = 1,
        watch_bucket: Optional[str] = None,  # DO NOT USE
    ) -> None:
        self.func = func
        self.id = id
        self.name = func.__name__
        self.replicas = replicas
        self.ack_wait_secs = ack_wait * 60

        if watch_bucket is not None:
            raise RuntimeError("to use a watch_bucket, use the new application construction style")

    def wire_up(self, sources: Iterable[EdgeFrom]) -> "Task":
        """
        Used when we're constructing a dag out of the tasks.
        """
        assert legacy_context.current_legacy_app is not None

        app = legacy_context.current_legacy_app.real_app

        factory = app.task()(self.func)

        # Note that since we're using self.id, we don't really create a new
        # instance if we wire up multiple times. This is bug-compatible with the legacy code.
        instance = factory(
            root_instance_name=self.id, replicas=self.replicas, ack_wait_secs=self.ack_wait_secs
        )

        for src in sources:
            app.edge(src, instance)

        return instance


class LegacyContext:
    """
    Built up from the various legacy @app and @task decorators in the code.

    New code should not rely on this, instead use a seaplane.pipes.App object to
    provide context for individual deployments and executions.
    """

    def __init__(self) -> None:
        self.apps: List[LegacyAppsCompat] = []
        self.tasks: List[LegacyTaskCompat] = []
        self.current_legacy_app: Optional[LegacyAppsCompat] = None

    def add_app(self, app: LegacyAppsCompat) -> None:
        self.apps.append(app)
        log.debug(f"App: {app.id}")

    @contextmanager
    def using_current_app(self, app: LegacyAppsCompat) -> Generator[None, None, None]:
        self.current_legacy_app = app
        yield
        self.current_legacy_app = None


legacy_context = LegacyContext()


def app(
    type: str = "API",
    parameters: Optional[List[str]] = None,
    id: Optional[str] = None,
    path: Optional[str] = None,
    _func: Optional[Callable[[Any], Any]] = None,
) -> Callable[[Callable[..., Any]], LegacyAppsCompat]:
    if path is not None:
        warn("The app path argument is deprecated", DeprecationWarning, stacklevel=2)
    if parameters is None:
        parameters = []

    if type != "API" or parameters != []:
        raise RuntimeError(
            "non API apps are not supported."
            " To listen to arbitrary streams, please use the new app construction tools."
        )

    def wrap_legacy_app_function(func: Callable[[Any], Any]) -> LegacyAppsCompat:
        set_id = id if id is not None else func.__name__.replace("_", "-")
        legacy_app = LegacyAppsCompat(func=func, id=set_id, type=type, parameters=parameters)
        legacy_context.add_app(legacy_app)

        return legacy_app

    if not _func:
        return wrap_legacy_app_function
    else:
        return wrap_legacy_app_function(_func)  # type: ignore


class TakeEdgeFroms(Protocol):
    def __call__(self, *args: EdgeFrom) -> Task:
        ...


def task(
    id: Optional[str] = None,
    watch_bucket: Optional[str] = None,
    type: Optional[str] = None,  # UNUSED
    model: Optional[str] = None,  # UNUSED
    index_name: Optional[str] = None,  # UNUSED
    replicas: int = 1,
    ack_wait: int = 2,
    _func: Optional[Callable[[Any], Any]] = None,
) -> Callable[[Callable[..., Any]], TakeEdgeFroms]:
    deprecated_args = {"type": type, "model": model, "index_name": index_name}
    for arg in deprecated_args:
        if deprecated_args[arg] is not None:
            warn(f"The task {arg} argument is deprecated", DeprecationWarning, stacklevel=2)

    def decorator_task(func: Callable[..., Any]) -> TakeEdgeFroms:
        task_id = id if id is not None else func.__name__.replace("_", "-")

        task = LegacyTaskCompat(
            func=func,
            id=task_id,
            replicas=replicas,
            ack_wait=ack_wait,
            watch_bucket=watch_bucket,
        )

        @functools.wraps(func)
        def wrapper(*sources: EdgeFrom) -> Task:
            return task.wire_up(sources)

        return cast(TakeEdgeFroms, wrapper)

    if not _func:
        return decorator_task
    else:
        return decorator_task(_func)  # type: ignore
