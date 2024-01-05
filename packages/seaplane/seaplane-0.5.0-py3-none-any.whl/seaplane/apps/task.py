from typing import Any, Callable, List, Optional
from seaplane.errors import SeaplaneError

from seaplane.logs import log

"""
Tasks are weird use / mention hybrids: in a deployment
context, they are a map of Seaplane carrier flows and
the connections between them. In an execution context
on the Seaplane platform, they're containers for executable
code that get the results of endpoints or tasks as input and can
emit good things to their downstream flows and endpoints.
"""


class Task:
    def __init__(
        self,
        func: Callable[[Any], Any],
        id: str,
        ack_wait: Optional[int] = 8,
        replicas: Optional[int] = 1,
        watch_bucket: Optional[str] = None,
    ) -> None:
        self.func = func
        self.id = id
        self.name = func.__name__
        self.replicas = replicas
        self.ack_wait = ack_wait
        self.watch_bucket = watch_bucket
        self.sources: List[str] = []

    def process(self, *args: Any, **kwargs: Any) -> Any:
        """
        Just executes the task code. Runs on the Seaplane infrastructure.
        """
        log.info(f"Task '{self.id}' processing...")
        return self.func(*args, **kwargs)

    def called_from(self, sources: List[str]) -> None:
        """
        Used when we're constructing a dag out of the tasks.
        """
        if sources and self.watch_bucket:
            raise SeaplaneError(
                f"task {self.id} is watching a bucket, it can't be wired to another task"
            )

        self.sources += sources

    def uses_endpoint(self) -> bool:
        """
        Only works after this task has been assembled into an app.
        """
        return "entry_point" in self.sources
