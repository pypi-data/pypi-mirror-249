from typing import Any, Generator, List, Optional
from importlib.metadata import version
import json
import os
import sys

import toml

from seaplane.apps.debug_schema import build_debug_schema
from seaplane.apps.decorators import legacy_context
from seaplane.apps.status import status
from seaplane.logs import log
from seaplane.pipes.executor import execute_task, TaskContext
from seaplane.deploy import deploy, destroy

# importing this because it loads our .env file as a side effect
from seaplane.config import config  # noqa: F401


class LegacyTaskContextAdapter:
    """
    LegacyTaskContextAdapter is given to tasks running in legacy mode.
    """

    def __init__(self, parent: TaskContext):
        self.parent = parent
        self.queue: List[Optional[bytes]] = []

    def emit(self, message: bytes, batch_id: Any = None) -> None:
        """Queues message to send once the task completes."""
        if batch_id is not None:
            raise RuntimeError(
                "Explicit batch ids are no longer supported."
                " Batch ids will be associated automatically with output"
            )

        self.queue.append(message)

    def cont(self) -> None:
        """Continues a task without emitting anything."""
        self.queue.append(None)

    @property
    def request_id(self) -> str:
        return self.parent.request_id

    @property
    def object_data(self) -> bytes:
        return self.parent.object_data

    @property
    def body(self) -> bytes:
        return self.parent.body


def _start_task(task_id: str) -> None:
    log.logger.info(f"executing task in legacy mode: {task_id}")

    task = None
    for compat in legacy_context.apps:
        compat.assemble()

    for compat in legacy_context.apps:
        app = compat.real_app

        if task_id in app.task_registry:
            task = app.task_registry[task_id]
            break

    if task is None:
        raise RuntimeError(f"no task found with id {task_id}")

    def legacy_task(root_context: TaskContext) -> Generator[Any, None, None]:
        tc_adapter = LegacyTaskContextAdapter(root_context)
        task.work(tc_adapter)

        for message in tc_adapter.queue:
            yield message

    execute_task(task.instance_name, legacy_task)


def start() -> None:
    """
    This is a legacy entry point. Prefer "App.run()" for new developments.

    *Run Locally*, this function builds, deploys, and manages a customer application.
    Run on seaplane infrastructure with no arguments, this function
    runs a user @task in a loop, pulling information upstream from the seaplane platform.
    """

    log.info(f"\n\n\tSeaplane Apps version {version('seaplane')}, Legacy 0.5 mode\n")

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "build":
            for compat in legacy_context.apps:
                compat.assemble()

            debug_schema = build_debug_schema([compat.real_app for compat in legacy_context.apps])
            print(json.dumps(debug_schema, indent=2))

        elif command == "deploy":
            pyproject = toml.loads(open("pyproject.toml", "r").read())
            project_directory_name = pyproject["tool"]["poetry"]["name"]
            for compat in legacy_context.apps:
                compat.assemble()

            for compat in legacy_context.apps:
                deploy(compat.real_app, project_directory_name)

            legacy_schema = build_debug_schema([compat.real_app for compat in legacy_context.apps])
            with open(os.path.join("build", "schema.json"), "w") as file:
                json.dump(legacy_schema, file, indent=2)

        elif command == "destroy":
            for compat in legacy_context.apps:
                compat.assemble()

            for compat in legacy_context.apps:
                destroy(compat.real_app)

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

    task_id = os.getenv("TASK_ID") or os.getenv("INSTANCE_NAME")

    if not task_id:
        log.debug("ERROR: Could not find TASK_ID or INSTANCE_NAME value")
        log.error(
            "Executing a Smartpipe workflow from outside a "
            + "Seaplane Deployment is not currently supported!"
        )
        sys.exit(-1)

    log.info(f"Starting Task {task_id} ...")
    _start_task(task_id)
    return None
