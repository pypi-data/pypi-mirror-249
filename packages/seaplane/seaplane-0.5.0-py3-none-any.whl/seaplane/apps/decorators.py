import functools
from typing import Any, Callable, Dict, List, Optional
from warnings import warn

from seaplane.config import config
from seaplane.logs import log

from .app import App
from .executor import RealTaskExecutor, TaskExecutor
from .task import Task


def task_to_json(task: Task) -> Dict[str, Any]:
    return {"id": task.id, "replicas": task.replicas}


def app_to_json(app: App) -> Dict[str, Any]:
    return {
        "id": app.id,
        "type": app.type,
        "parameters": app.parameters,
        "tasks": [task_to_json(task) for task in app.tasks],
    }


def apps_json(apps: List[App]) -> Dict[str, Any]:
    return {
        "type": "apps",
        "payload": [app_to_json(app) for app in apps],
    }


class Context:
    """
    Built up from the various @app and @task decorators in the code.
    """

    def __init__(
        self,
        apps: Optional[List[App]] = None,  # TODO unused?
        tasks: Optional[List[Task]] = None,  # TODO unused?
    ) -> None:
        self.actual_app_index = -1
        self.task_executor: TaskExecutor = RealTaskExecutor()

        if apps is None:
            self.apps = []
        else:
            self.apps = apps

        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks

    def active_app(self, id: str) -> None:
        for i, app in enumerate(self.apps):
            if app.id == id:
                self.actual_app_index = i
                break

    def get_actual_app(self) -> Optional[App]:
        if self.actual_app_index == -1:
            return None

        return self.apps[self.actual_app_index]

    def add_app(self, app: App) -> None:
        self.actual_app_index = len(self.apps)
        self.apps.append(app)
        log.debug(f"App: {app.id}")

    def add_task(self, task: Task) -> None:
        log.debug(f"⌛️ Task {task.id} with {task.replicas} replicas")
        self.tasks.append(task)

    def get_task(self, id: str) -> Optional[Task]:
        for c in self.tasks:
            if c.id == id:
                return c

        return None

    def assign_to_active_app(self, task: Task) -> None:
        self.apps[self.actual_app_index].add_task(task)
        app = context.get_actual_app()
        if app is not None:
            log.info(f"⌛️ Assign Task {task.id} to App: {app.id}")
        else:
            log.info(
                f"🔥 Actual App is None, can't assign \
                    Task {task.id} to App"
            )

    def set_executor(self, executor: TaskExecutor) -> None:
        self.task_executor = executor


context = Context()


def app(
    type: str = "API",
    parameters: Optional[List[str]] = None,
    id: Optional[str] = None,
    path: Optional[str] = None,
    _func: Optional[Callable[[Any], Any]] = None,
) -> Callable[[Any, Any], Any]:
    if path is not None:
        warn("The app path argument is deprecated", DeprecationWarning, stacklevel=2)
    if parameters is None:
        parameters = []

    def decorator_apps(func: Callable[[Any], Any]) -> Callable[[Any, Any], Any]:
        root_id = id if id is not None else func.__name__.replace("_", "-")
        set_id = config.name_prefix + root_id

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            context.active_app(set_id)
            return func(*args, **kwargs)

        app = App(func=wrapper, id=set_id, type=type, parameters=parameters)
        context.add_app(app)
        return wrapper

    if not _func:
        return decorator_apps  # type: ignore
    else:
        return decorator_apps(_func)


def task(
    id: Optional[str] = None,
    watch_bucket: Optional[str] = None,
    type: Optional[str] = None,  # UNUSED
    model: Optional[str] = None,  # UNUSED
    index_name: Optional[str] = None,  # UNUSED
    replicas: Optional[int] = 1,
    ack_wait: Optional[int] = 2,
    _func: Optional[Callable[[Any], Any]] = None,
) -> Callable[[Any, Any], Any]:
    deprecated_args = {"type": type, "model": model, "index_name": index_name}
    for arg in deprecated_args:
        if deprecated_args[arg] is not None:
            warn(f"The task {arg} argument is deprecated", DeprecationWarning, stacklevel=2)

    def decorator_task(func: Callable[[Any], Any]) -> Callable[[Any, Any], Any]:
        root_id = id if id is not None else func.__name__.replace("_", "-")
        task_id = config.name_prefix + root_id

        task = Task(
            func=func,
            id=task_id,
            replicas=replicas,
            ack_wait=ack_wait,
            watch_bucket=watch_bucket,
        )
        context.add_task(task)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            context.assign_to_active_app(task)

            return context.task_executor.execute(task, *args, **kwargs)

        return wrapper

    if not _func:
        return decorator_task  # type: ignore
    else:
        return decorator_task(_func)
