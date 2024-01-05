import json
import os
import shutil
import toml
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from seaplane.sdk_internal_utils.buckets import create_bucket_if_needed
from seaplane.deploy.utils import (
    create_flow,
    delete_flow,
    create_stream,
    delete_stream,
    add_secrets,
    upload_project,
)

# THIS IS BEING REPLACED! SEE seaplane.deploy for replacement code and systems.

from seaplane.config import Configuration, config, runner_image
from seaplane.logs import log

from .app import App
from .debug_schema import build_debug_schema
from .decorators import context
from .task import Task
from .executor import SchemaExecutor

ENDPOINTS_STREAM = "_SEAPLANE_ENDPOINT"


def endpoints_input_subject(app_id: str) -> str:
    """
    The default stream name for the application as a whole. Requests to the
    app endpoint will end up on this stream.
    """
    return f"{ENDPOINTS_STREAM}.in.{app_id}.*"


def endpoints_output_subject(app_id: str) -> str:
    """
    The default output stream for the app as a whole, and for this
    request id in particular.
    """
    # The following ${! ... } incantations are Benthos function interpolation
    request_id = '${! meta("_seaplane_request_id") }'
    joined_batch_hierarchy = '${! meta("_seaplane_batch_hierarchy") }'
    return f"{ENDPOINTS_STREAM}.out.{app_id}.{request_id}{joined_batch_hierarchy}"


def task_subject(app_id: str, task_id: str) -> str:
    return f"{app_id}.{task_id}"


def build_task_flow_config(
    app: App,
    task: Task,
    project_url: str,
    bucket_subjects: Dict[str, str],  # mapping of bucket name to notification stream name
) -> Dict[str, Any]:
    if task.uses_endpoint() and app.type == "stream":  # User override
        input = app.parameters[0]
    elif task.watch_bucket is not None:  # Bind to watch bucket
        input = bucket_subjects[task.watch_bucket]
    elif task.uses_endpoint():  # read from the endpoint default stream
        input = endpoints_input_subject(app.id)
    else:  # listen to interior wire-ups
        input = task_subject(app.id, task.id)

    carrier_output: Optional[Dict[str, Any]] = None

    next_subjects = [
        task_subject(app.id, peer.id) for peer in app.tasks if task.id in peer.sources
    ]
    if app.returns == task.id:
        next_subjects.append(endpoints_output_subject(app.id))

    if len(next_subjects) > 1:
        carrier_output = {
            "broker": {"outputs": [{"carrier": {"subject": subject}} for subject in next_subjects]}
        }
    elif len(next_subjects) == 1:
        carrier_output = {
            "carrier": {"subject": next_subjects[0]},
        }
    output = {
        "switch": {
            "cases": [
                {
                    "check": 'meta("_seaplane_drop") == "True"',
                    "output": {"drop": {}},
                },
                {
                    "check": 'meta("_seaplane_drop") != "True"',
                    "output": carrier_output,
                },
            ]
        }
    }

    ack_wait = f"{str(task.ack_wait)}m"

    workload = {
        "input": {
            "carrier": {
                "stream": input.split(".", 1)[0],
                "subject": input,
                "durable": task.id,
                "ack_wait": ack_wait,
                "bind": True,
            },
        },
        "processor": {
            "docker": {
                "image": runner_image(),
                "args": [project_url],
            }
        },
        "output": output,
        "replicas": task.replicas,
    }

    log.debug(f"Created {task.id} workload")
    log.debug(json.dumps(workload, indent=2))

    return workload


def get_secrets(config: Configuration) -> Dict[str, str]:
    secrets = {}
    for key, value in config._api_keys.items():
        secrets[key] = value

    return secrets


def print_endpoints(apps: List[App]) -> None:
    endpoint_apps = [a for a in apps if any(task.uses_endpoint() for task in a.tasks)]
    if len(endpoint_apps) > 0:
        log.info("\nDeployed Endpoints:\n")

    for app in endpoint_apps:
        if app.type == "API":
            log.info(
                f"{app.id} Endpoint: POST "
                f"https://{urlparse(config.carrier_endpoint).netloc}/v1/endpoints/{app.id}/request"
            )
            log.info(
                f"{app.id} CLI Command: plane endpoints request {app.id} -d <data> OR @<file>"
            )
        elif app.type == "stream" and len(app.parameters) >= 1:
            log.info(f"🚀 {app.id} using stream subject {app.parameters[0]} as entry point")

    if len(endpoint_apps) > 0:
        print("\n")


def deploy_task(
    app: App,
    task: Task,
    secrets: Dict[str, str],
    bucket_subjects: Dict[str, str],  # mapping of bucket names to their associated notify subjects
    project_url: str,
) -> None:
    delete_flow(task.id)

    workload = build_task_flow_config(app, task, project_url, bucket_subjects)

    create_flow(task.id, workload)
    secrets = secrets.copy()
    secrets["TASK_ID"] = task.id
    add_secrets(task.id, secrets)

    # Log some useful info about where this is deployed
    #  Note that region info is only included if we have set it
    deploy_info = ""
    if "staging" in config.carrier_endpoint:
        deploy_info += " in staging"
    if config.dc_region is not None:
        deploy_info += f" in {config.dc_region} data center"
    log.info(f"Deploy for task {task.id} done{deploy_info}")


def run_deploy() -> None:
    """
    Top level task for deploying an application, called from the CLI.
    Writes files, posts and destroys new Seaplane resources, writes logs.
    """
    secrets = get_secrets(config)
    if not config._token_api.api_key:
        log.info("API KEY not set. Please set in .env or seaplane.config.set_api_key()")
        return

    shutil.rmtree("build/", ignore_errors=True)

    # Spider the apps and tasks finalize their structure.
    context.set_executor(SchemaExecutor())
    for app in context.apps:
        app.assemble()

    # Create buckets and get associated notify subjects if necessary.
    bucket_subjects = {}
    for app in context.apps:
        for task in app.tasks:
            if task.watch_bucket:
                bucket_subjects[task.watch_bucket] = create_bucket_if_needed(
                    app.id, task.watch_bucket
                )

    # Write out schema for use with other tooling
    debug_schema = build_debug_schema(context.apps)

    if not os.path.exists("build"):
        os.makedirs("build")

    with open(os.path.join("build", "schema.json"), "w") as file:
        json.dump(debug_schema, file, indent=2)

    # use the apps and tasks directly for the rest of the deployment
    debug_schema = None  # type: ignore

    # Upload project assets
    pyproject = toml.loads(open("pyproject.toml", "r").read())
    project_url = upload_project(pyproject["tool"]["poetry"]["name"])

    deploy_info = ""
    if "staging" in config.carrier_endpoint:
        deploy_info += " in staging"
    if config.region is not None:
        deploy_info += f" in {config.region} region"

    log.info(f"Deploying everything{deploy_info}...")

    bucket_streams = {v.split(".", 1)[0] for v in bucket_subjects.values()}
    for stream in bucket_streams:
        delete_stream(stream)
        create_stream(stream)

    for app in context.apps:
        delete_stream(app.id)
        create_stream(app.id)

        for task in app.tasks:
            deploy_task(app, task, secrets, bucket_subjects, project_url)

    print_endpoints(context.apps)

    log.info("🚀 Deployment complete")


def destroy() -> None:
    """
    Top level call to delete Seaplane resources associated with this project.
    """
    if not config._token_api.api_key:
        log.info("API KEY not set. Please set in .env or seaplane.config.set_api_key()")
        return

    # Consider loading the existing schema like status when you destroy
    context.set_executor(SchemaExecutor())
    for app in context.apps:
        app.assemble()

    for app in context.apps:
        delete_stream(app.id)

        for task in app.tasks:
            delete_flow(task.id)
