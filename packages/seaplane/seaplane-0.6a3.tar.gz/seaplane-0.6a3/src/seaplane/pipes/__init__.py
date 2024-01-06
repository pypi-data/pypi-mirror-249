import os
from typing import Any, Callable, Dict, Iterable, Optional, Set, Union
from seaplane.config import config
from seaplane.errors import SeaplaneError
from seaplane.logs import log

from seaplane.sdk_internal_utils.buckets import create_bucket_if_needed

from .executor import execute_task


"""
SDK Tasks are mapped to Seaplane flows. To define a flow, use code like the following:

# Tasks live in the scope of an app, which is also a unit
# of task deployment.
app = seaplane.pipes.App("my-app")

@app.task
def repeat_input(context):
    # This code will be run on the seaplane infrastructure.
    # The context will contain messages from upstream
    # in Seaplane carrier, and this code will yield
    # messages to its downstream listeners
    repeated = context.body + context.body
    yield repeated


# You can create individual instances of a task
# by calling it like a function. Be aware that you're *not*
# calling the function that you defined! Instead you're
# defining a unit of deployment.
repeat_input_flow = repeat_input()


# To wire the flow into other flows, use the >> operator

# read input messages from the seaplane input endpoint
app.input() >> repeat_input_flow

# push the results to the seaplane output endpoint
repeat_input_flow >> app.output()
"""


class Subject:
    """
    Subject is a base pubsub subject.

    Subject should represent a concrete, publishable subject - it can
    contain fun ${! meta} macros, but should not contain wildcards.

    Tasks can write to subjects but not subscribe to them.

    my_task() >> Subject("known-stream.explicit-subject")
    """

    def __init__(self, subject: str):
        self.subject = subject

    def __hash__(self) -> int:
        return hash(self.subject)

    def __eq__(self, other: Any) -> Any:
        return self.subject == other.subject

    def __rshift__(self, _: Any) -> Any:  # >>
        raise SeaplaneError(
            "Subjects can be written to but not read from. Use a Subscription in this case."
        )

    def __lshift__(self, other: Any) -> Any:  # <<
        if not isinstance(other, Task):
            raise SeaplaneError(
                f"can't send messages directly {self.subject} << {other}"
                ". All messages must pass through a task."
            )

        return other >> self


class Subscription:
    """
    The possibly-filtered name of a subject, for matching.

    Should not ever contain macros and things, but may contain wildcards.

    Tasks can subscribe to Subscriptions but not write to them.

    Subscription("known-stream.explicit-subscription.>") >> my_task()
    """

    def __init__(self, filter: str):
        self.filter = filter

    def __hash__(self) -> int:
        return hash(self.filter)

    def __eq__(self, other: Any) -> Any:
        return self.filter == other.filter

    def __rshift__(self, other: Any) -> Any:  # >>
        if not isinstance(other, Task):
            raise SeaplaneError(
                f"can't send messages directly {self.filter} >> {other}"
                ". All messages must pass through a task."
            )

        return other << self

    def __lshift__(self, _: Any) -> Any:  # <<
        raise SeaplaneError(
            "Subscriptions can be read from but not written to. Use a Subject in this case."
        )

    def stream(self) -> str:
        return self.filter.split(".", 1)[0]


class OutEndpoint(Subject):
    """The output seaplane endpoint. Does not accept subscriptions."""

    def __init__(self, endpoint: str):
        super(OutEndpoint, self).__init__(
            f"_SEAPLANE_ENDPOINT.out.{endpoint}."
            '${! meta("_seaplane_output_id") }'
            '${! meta("_seaplane_batch_hierarchy") }'
        )


class InEndpoint(Subscription):
    """Endpoint represents the Subject of a seaplane input endpoint."""

    def __init__(self, endpoint: str):
        super(InEndpoint, self).__init__(f"_SEAPLANE_ENDPOINT.in.{endpoint}.>")
        self.endpoint = endpoint


class _TaskSubject(Subject):
    """Task subjects conform to a standard format

    app.task.address-tag.output_id.batch.batch.batch
    """

    def __init__(self, app_name: str, instance_name: str):
        self.app_name = app_name
        self.instance_name = instance_name
        super(_TaskSubject, self).__init__(
            f"{app_name}.{instance_name}"
            '.${! meta("_seaplane_address_tag") }'
            '.${! meta("_seaplane_output_id") }'
            '${! meta("_seaplane_batch_hierarchy") }'
        )

    # TODO support output addresses in customer code
    def task_subscription(self, address: str) -> Subscription:
        """use address = '*' to match all outputs from this task"""
        return Subscription(f"{self.app_name}.{self.instance_name}.{address}.>")


class Bucket:
    """
    A reference to a bucket and it's associated notification subscription.

    Get a bucket by asking the app to query the Seaplane infrastructure, like this:

    app = App("bucket-demo-app")

    # This queries the Seaplane infrastructure, and may creaet a bucket
    # if one doesn't exist already
    bucket = app.bucket("bucket-demo-bucket")

    bucket >> task()
    """

    def __init__(self, name: str, notify: str):
        self.name = name
        self.notify_subscription = Subscription(notify)

    def __rshift__(self, other: Any) -> Any:
        return self.notify_subscription >> other


class Task:
    """
    Description of deployment intent associated with an instance of a task.

    Tasks map to Seaplane flows when deployed.

    Create tasks through an App, like this

    app = App("task-demo")

    @app.task()
    def do_it(context):
        print("done!")

    # Notice that the task is an *instance* of do_it(), there can be
    # more than one.
    my_task = do_it()
    """

    def __init__(
        self,
        app: "App",
        work: Callable[..., Any],
        instance_name: str,
        subject: _TaskSubject,
        replicas: int,
        ack_wait_secs: int,
    ):
        # Note that app is a circular reference, so Tasks will not be GC'd
        self.app = app
        self.work = work
        self.instance_name = instance_name
        self.subject: Subject = subject  # task output
        self.replicas = replicas
        self.ack_wait_secs = ack_wait_secs
        self.subscriptions: Set[Subscription] = set()  # pull input from these subjects

    def subscribe(self, source: Subscription) -> None:
        self.subscriptions.add(source)

    def __rshift__(self, other: Any) -> Any:  # >>
        self.app.edge(self, other)
        return None

    def __lshift__(self, other: Any) -> Any:  # <<
        self.app.edge(other, self)
        return None


class TaskFactory:
    """
    An association between an app and a python function, that can
    be made into a flow for deploying on the Seaplane infrastructure.

    Create a TaskFactory by annotating a function with `app.task`, like this:

    app = App("taskfactory-demo")

    @app.task()
    def do_it(context):
        ...

    Now `do_it` is a TaskFactory that you can use to create Task instances
    and wire them to other Task instances and subjects in the Seaplane infrastructure.

    """

    def __init__(self, app: "App", work: Callable[..., Any], task_name: str):
        self.app = app
        self.work = work
        self.task_name = task_name

    def __call__(
        self,
        root_instance_name: Optional[str] = None,
        replicas: int = 1,
        ack_wait_secs: int = 8 * 60,
    ) -> Task:
        if root_instance_name is None:
            root_instance_name = f"{self.task_name}-default"

        instance_name = self.app.name_prefix + root_instance_name
        subject = _TaskSubject(self.app.name, instance_name)

        if instance_name in self.app.task_registry:
            ret = self.app.task_registry[instance_name]
            if ret.replicas != replicas or ret.ack_wait_secs != ack_wait_secs:
                log.logger.warning(
                    f"task {ret.instance_name} has been configured in two different ways."
                    f" Using {ret.replicas} replicas and {ret.ack_wait_secs} ack_wait_secs"
                )

        else:
            ret = Task(
                self.app,
                self.work,
                instance_name,
                subject,
                replicas,
                ack_wait_secs,
            )
            self.app.task_registry[ret.instance_name] = ret

        return ret

    def __lshift__(self, other: Any) -> Any:  # <<
        self.app.edge(other, self)
        return None

    def __rshift__(self, other: Any) -> Any:  # >>
        self.app.edge(self, other)
        return None


EdgeFrom = Union[Task, TaskFactory, Bucket, Subscription]
EdgeTo = Union[Task, TaskFactory, Subject]


class App:
    """
    App is a namespace and unit of deployment for
    a collection of Tasks. Apps create a namespace for task messages
    and manage deployment together.
    """

    # Global registry of all known apps.
    _REGISTRY: Dict[str, "App"] = {}

    def __init__(self, name: str, name_prefix: Optional[str] = None):
        """Create a new `App`.

        Creates a new `App` named `name`. Initializes an empty task
        registry and registers the app in the process-wide registry.

        if name_prefix is provided, stream and task names will use that
        prefix.
        """
        if name_prefix is None:
            name_prefix = config.name_prefix

        self.name_prefix = name_prefix
        self.name = name_prefix + name
        self.buckets: Set[Bucket] = set()
        self.task_registry: Dict[str, Task] = {}
        self._REGISTRY[name] = self
        self.input_endpoint = InEndpoint(self.name)
        self.output_endpoint = OutEndpoint(self.name)

    @classmethod
    def all(cls) -> Iterable["App"]:
        return cls._REGISTRY.values()

    def task(self) -> Callable[..., TaskFactory]:
        """Task wraps and registers a task."""

        def _wrapper(func: Callable[..., Any]) -> TaskFactory:
            taskname = func.__name__.replace("_", "-")
            return TaskFactory(self, func, taskname)

        return _wrapper

    def input(self) -> InEndpoint:
        """Return the "in" `Endpoint` for this App."""
        return self.input_endpoint

    def output(self) -> OutEndpoint:
        """Return the "out" `Endpoint` for this App."""
        return self.output_endpoint

    def bucket(self, bucket_name: str) -> Bucket:
        """
        Return a notify-capable bucket.

        Makes a network request to the Seaplane object store. Will
        attempt to create a new bucket if one doesn't exist, and may
        fail with an Exception if there is a service failure or if
        the named bucket exists but is not configured to send notifications.
        """

        notify = create_bucket_if_needed(self.name, bucket_name)
        b = Bucket(bucket_name, notify)
        self.buckets.add(b)
        return b

    def edge(
        self,
        source: EdgeFrom,
        dest: EdgeTo,
    ) -> None:
        """
        Add an edge from a to b, binding b to a's output.

        Tasks can be wired to publish informatino to other tasks and explicit subjects.
        Tasks can be wired to recieve information from other tasks, subscriptions, or
        bucket notifications.
        """

        if isinstance(source, TaskFactory):
            source = source()

        if isinstance(dest, TaskFactory):
            dest = dest()

        # Type tomfoolery is for ergonomics
        if not (isinstance(source, Task) or isinstance(dest, Task)):
            raise RuntimeError("edges must pass through a task")

        if isinstance(dest, Bucket):
            raise SeaplaneError("tasks can listen to buckets, but buckets can't listen to tasks")

        if isinstance(source, Subject):
            raise SeaplaneError(
                "the first argument to edge must be a Task, Bucket, or Subscription"
            )

        if isinstance(dest, Subscription):
            raise SeaplaneError("the second argument to edge must be a Task or a Subject")

        if isinstance(source, Bucket):
            source = source.notify_subscription

        if isinstance(source, Task) and isinstance(dest, Task):
            # TODO the lhs of an edge should be parameterized by the address
            # TODO already, so do some similar "Subscription" -> "AddressedSubscription"
            # TODO foolery here.
            if isinstance(source.subject, _TaskSubject):
                # This is a typical, addresssable subject that we know how to match
                source = source.subject.task_subscription("*")
            else:
                raise SeaplaneError(
                    f"can't listen to task subject {source.subject.subject} automatically."
                    " To listen to this, you'll need to use an explicit Subscription"
                    " and write the Seaplane carrier filter yourself"
                )

        if isinstance(source, Task) and isinstance(dest, Subject):
            source.subject = dest

        elif isinstance(source, Subscription) and isinstance(dest, Task):
            dest.subscribe(source)
        else:
            raise AssertionError("unreachable")

    def run(self) -> None:
        """
        Run the application as the main work of a process.

        Reads command line arguments and the INSTANCE_NAME environment variable. If INSTANCE_NAME
        is present, will attempt to execute the associated task, otherwise will
        print out the structure of the application.
        """
        # This has a bunch of circular dependencies but the ergonomics of `app.run()`
        # seem to make it worthwhile.
        import sys
        import tabulate
        import toml

        import seaplane.deploy
        import seaplane.run_load_dotenv

        command = None
        if len(sys.argv) > 1:
            command = sys.argv[1]

        instance_name = os.getenv("INSTANCE_NAME")

        if command == "deploy":
            pyproject = toml.loads(open("pyproject.toml", "r").read())
            project_directory_name = pyproject["tool"]["poetry"]["name"]
            seaplane.deploy.deploy(self, project_directory_name)
        elif command == "destroy":
            seaplane.deploy.destroy(self)
        elif instance_name:
            task = self.task_registry[instance_name]
            execute_task(task.instance_name, task.work)
        else:
            rows = []
            for task in self.task_registry.values():
                rows.append(
                    (
                        ",".join(x.filter for x in task.subscriptions),
                        "=>",
                        task.instance_name,
                        "->",
                        task.subject.subject,
                    )
                )
            print(tabulate.tabulate(rows, headers=["input", "", "task", "", "output"]))
