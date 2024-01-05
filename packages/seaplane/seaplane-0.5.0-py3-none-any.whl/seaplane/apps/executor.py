from typing import cast, Any

from .task import Task


class TaskExecutor:
    def execute(self, task: Task, *args: Any, **kwargs: Any) -> Any:
        pass


class RealTaskExecutor(TaskExecutor):
    def __init__(self) -> None:
        ...

    def execute(self, task: Task, *args: Any, **kwargs: Any) -> Any:
        return task.process(*args, **kwargs)


class SchemaExecutor(TaskExecutor):
    def __init__(self) -> None:
        ...

    def execute(self, task: Task, *args: Any, **kwargs: Any) -> Any:
        task.called_from([cast(str, a) for a in args])
        return task.id
