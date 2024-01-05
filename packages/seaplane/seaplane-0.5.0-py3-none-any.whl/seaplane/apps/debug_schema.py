from typing import Any, Dict, List

from seaplane.config import config
from seaplane.apps.app import App


def build_debug_schema(apps: List[App]) -> Dict[str, Any]:
    """
    Constructs a JSON-friendly / simple type structure describing
    the project by running the application SchemaExecutors and analysing
    the resulting structure of apps and tasks.

    Apps and their tasks must be fully assembled before passing them here.
    """
    schema: Dict[str, Any] = {"apps": {}}

    for app in apps:
        app_desc: Dict[str, Any] = {
            "id": app.id,
            "entry_point": {"type": app.type, "parameters": app.parameters},
            "tasks": [],
            "io": {},
        }

        for task in app.tasks:
            task_desc = {
                "id": task.id,
                "name": task.name,
                "replicas": task.replicas,
                "ack_wait": task.ack_wait,
            }

            # app_desc["io"] is a table from source tasks to their downstreams.
            # we hope there is no source named "returns"
            for source in task.sources:
                if not app_desc["io"].get(source, None):
                    app_desc["io"][source] = [task.id]
                else:
                    app_desc["io"][source].append(task.id)

            app_desc["tasks"].append(task_desc)

        app_desc["io"]["returns"] = app.returns
        schema["apps"][app.id] = app_desc

    schema["carrier_endpoint"] = config.carrier_endpoint
    schema["identity_endpoint"] = config.identify_endpoint

    return schema
