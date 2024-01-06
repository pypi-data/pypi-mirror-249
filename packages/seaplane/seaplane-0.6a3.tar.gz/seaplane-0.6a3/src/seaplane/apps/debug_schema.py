from typing import Any, Dict, List

from seaplane.config import config
from seaplane.pipes import App


def build_debug_schema(apps: List[App]) -> Dict[str, Any]:
    """
    Constructs a JSON-friendly / simple type structure describing
    some parts of the application for use by associated tooling.
    """
    # This is a legacy debug schema, and it's structure shouldn't be
    # relied on.

    schema: Dict[str, Any] = {"apps": {}}

    for app in apps:
        app_desc: Dict[str, Any] = {
            "id": app.name,
            "tasks": [],
        }

        for task in app.task_registry.values():
            task_desc = {
                "id": task.instance_name,
                "name": task.work.__name__,
                "replicas": task.replicas,
            }

            app_desc["tasks"].append(task_desc)

        schema["apps"][app.name] = app_desc

    schema["carrier_endpoint"] = config.carrier_endpoint
    schema["identity_endpoint"] = config.identify_endpoint

    return schema
