from importlib.metadata import version
import json
import os
import sys
import traceback

from seaplane_framework.flow import processor

from seaplane.apps.debug_schema import build_debug_schema
from seaplane.apps.decorators import context
from seaplane.apps.deploy import run_deploy, destroy
from seaplane.apps.status import status
from seaplane.apps.executor import SchemaExecutor
from seaplane.apps.task_context import TaskContext
from seaplane.errors import SeaplaneError
from seaplane.logs import log

# importing this because it loads our .env file as a side effect
from seaplane.config import config  # noqa: F401


def _start_task(task_id: str) -> None:
    task = context.get_task(task_id)

    if not task:
        raise SeaplaneError(
            f"Task {task_id} not found, \
                            make sure the Task ID is correct."
        )

    processor.start()

    while True:
        log.info(f"Task {task.id} waiting for data...")

        # TODO: A read can fail if the incoming data is using
        #       a newer format than this version of `processor`
        #       understands. This would almost certainly be
        #       our fault, but we should still deadletter the message
        #       rather than crashing.
        message = processor.read()

        if "_seaplane_request_id" not in message.meta:
            # This must be the first task in a smartpipe, so we have to get the
            # Endpoints API generated request ID from the incoming nats_subject.
            request_id = message.meta["nats_subject"].split(".")[
                -1
            ]  # The Endpoints API always adds a request ID as the leaf
            message.meta["_seaplane_request_id"] = request_id

            # Similarly let's initialise the batch hierarchy to start out empty
            message.meta["_seaplane_batch_hierarchy"] = ""

        log.debug(f"{task.id} servicing {message.meta['_seaplane_request_id']}")

        task_context = TaskContext(message.body, message.meta)

        # TODO: Handle task errors gracefully
        try:
            task.process(task_context)
        except Exception as e:
            # At this point, the SDK user's code has thrown an exception
            # there's nothing we can do but log it and move on.
            # NB: We're not returning here, so any existing batch items
            # will still be written.
            error_str = "\n".join(traceback.format_exception(type(e), e, e.__traceback__))
            log.error(
                f"Error running Task:\
                \n {error_str}"
            )

        # The task may have written messages (by virtue of TaskContext.emit), so we now
        # flush them down the pipe.
        processor.flush()


def start() -> None:
    """
    *Run Locally*, this function builds, deploys, and manages a customer application.
    Run on seaplane infrastructure with no arguments, this function
    runs a user @task in a loop, pulling information upstream from the seaplane platform.
    """

    log.info(f"\n\n\tSeaplane Apps version {version('seaplane')}\n")

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "build":
            # For now, "build" doesn't support watch_buckets
            context.set_executor(SchemaExecutor())
            for app in context.apps:
                app.assemble()
            debug_schema = build_debug_schema(context.apps)
            print(json.dumps(debug_schema))
        elif command == "deploy":
            run_deploy()
        elif command == "destroy":
            destroy()
        elif command == "status":
            status()
        else:
            log.error(
                f"Found an invalid internal command `{command}`.\n"
                + "Expected one of: \n"
                + " - build\n"
                + " - deploy\n"
                + " - destroy\n"
                + " - status\n"
            )
        return None

    task_id = os.getenv("TASK_ID")

    if not task_id:
        log.debug("ERROR: Could not find TASK_ID value")
        log.error(
            "Executing a Smartpipe workflow from outside a "
            + "Seaplane Deployment is not currently supported!"
        )
        sys.exit(-1)

    log.info(f"Starting Task {task_id} ...")
    _start_task(task_id)
    return None
