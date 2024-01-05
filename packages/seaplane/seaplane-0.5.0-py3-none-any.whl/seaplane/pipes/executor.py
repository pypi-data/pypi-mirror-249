import time
import inspect
import json

from typing import cast, Any, Callable, Iterable, Optional

from seaplane_framework.flow import processor
from seaplane.logs import log
from seaplane.object import object_store


class TaskContext:
    """
    TaskContext is what a Task receives when running on the Seaplane platform.
    """

    def __init__(self, body: bytes, meta: dict[str, Any]):
        self.body = body
        # For now let's not imply that customers should touch this
        self._meta = meta
        self._object_data: Optional[bytes] = None

    @property
    def request_id(self) -> str:
        return cast(str, self._meta["_seaplane_request_id"])

    @property
    def object_data(self) -> bytes:
        """
        Attempts to interpret the body of the context
        as an object store event, and to syncronously load
        the associated object and return it.

        May throw exceptions if the message isn't an object store
        notification, if the object store is unavailable, or if
        the object store would otherwise throw an exception (for example,
        if the notification was for a deleted object.)
        """
        if self._object_data is not None:
            return self._object_data

        try:
            msg = json.loads(self.body)
            bucket = msg["Bucket"]
            obj = msg["Object"]
        except (json.JSONDecodeError, KeyError):
            log.logger.error(
                "it doesn't look like this message was from the object store."
                " Make sure your tasks are configured to listen to object store messages"
                " when using context.object_data"
            )
            raise

        self._object_data = object_store.download(bucket, obj)

        return self._object_data


def execute_task(task_name: str, work: Callable[..., Any]) -> None:
    """
    Execute the given task in an infinite loop. Never returns.

    Exceptions are logged but do not break the loop. execute_task
    doesn't return
    """
    processor.start()
    log.logger.info(f"{task_name} ready for processing")

    while True:
        try:
            message = processor.read()
            log.logger.debug(f"processing {message.body}")

            if "_seaplane_output_id" not in message.meta:
                # This must be the first task in a smartpipe, so we have to get the
                # Endpoints API generated request ID from the incoming nats_subject.
                request_id = message.meta["nats_subject"].split(".")[
                    -1
                ]  # The Endpoints API always adds a request ID as the leaf

                # TODO what if this is an object update or some other weird business?
                # TODO (maybe object updates have something useful in their metadata?)
                message.meta["_seaplane_request_id"] = request_id
                message.meta["_seaplane_output_id"] = request_id

            if "_seaplane_address_tag" not in message.meta:
                # TODO allow customer code to write address tags.
                message.meta["_seaplane_address_tag"] = "default"

            if "_seaplane_batch_hierarchy" not in message.meta:
                # Similarly let's initialise the batch hierarchy to start out empty
                message.meta["_seaplane_batch_hierarchy"] = ""

            task_context = TaskContext(message.body, message.meta.copy())
            result = work(task_context)

            # This complex return protocol is an attempt at user ergonomics.
            # If the user returns nothing or yields nothing, treat it like a drop.
            # If the user returns a generator, iterate over it.
            # If the user returns a non-None, generator, then treat it as a single returned result.

            if inspect.isgenerator(result):
                gen: Iterable[Any] = result
            else:
                gen = [result]

            batch_id = 1
            for output in gen:
                print(f"OUTPUT {repr(output)}")

                new_meta = message.meta.copy()

                if output is None:
                    new_meta["_seaplane_drop"] = "True"
                    output = b"None"
                    log.logger.info(
                        f'dropping output for "{new_meta["_seaplane_output_id"]}"'
                        " at user request"
                    )
                else:
                    new_meta["_seaplane_batch_hierarchy"] += f".{batch_id}"
                    batch_id += 1
                    log.logger.debug(
                        f'served "{new_meta["_seaplane_output_id"]}'
                        f'.{new_meta["_seaplane_batch_hierarchy"]}"'
                    )

                output_msg = processor._Msg(bytes(output), new_meta)
                processor.write(output_msg)
                processor.flush()

        except AssertionError:
            # Special case for ease in testing, and because we assume customer
            # code that fails assertions expects to crash.
            raise
        except Exception as e:
            log.logger.error(f"Error running Task {task_name}", exc_info=e)

            # We should revisit this exception handling, but for now
            # we just try not to spam whatever went wrong.
            # This will delay the `processor.flush()`, but it's
            # unlikely that we have anything interesting to flush
            # since we exploded.
            time.sleep(5)
