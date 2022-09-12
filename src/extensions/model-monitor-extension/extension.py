#!/usr/bin/env python3

import json
import os
import signal
import sys
from pathlib import Path

import requests
from model_monitor.logs_manager import LogsManager
from model_monitor.logs_subscriber import subscribe_to_ipc

# global variables
# extension name has to match the file's parent directory name)
LAMBDA_EXTENSION_NAME = Path(__file__).parent.name


def execute_custom_processing(event):
    """Logs record if condition is met.

    Args:
        event (json): event sent from lambda function.
    """
    print(f"[{LAMBDA_EXTENSION_NAME}] Received event: {json.dumps(event)}", flush=True)
    LogsManager.get_manager().send_batch()


# def execute_custom_shutdown(event): # pylint: disable=unused-argument
#     """Event to run when lambda wants to terminate.

#     Args:
#         event (json): event sent from lambda function.
#     """
#     print(f"[{LAMBDA_EXTENSION_NAME}] Received SHUTDOWN event. Exiting.", flush=True)
#     LogsManager.get_manager().send_batch()
#     print("Sent")

### boiler plate code below ###
def handle_signal(
    signal, frame
):  # pylint: disable=unused-argument,redefined-outer-name
    """
    Handles signal for a shutdown event.
    """
    # if needed pass this signal down to child processes
    print(f"[{LAMBDA_EXTENSION_NAME}] Received signal={signal}. Exiting.", flush=True)
    sys.exit(0)


def register_extension():
    """Register extension with the extension API

    Returns:
        _type_: Returns extension id.
    """
    print(f"[{LAMBDA_EXTENSION_NAME}] Registering...", flush=True)
    headers = {
        "Lambda-Extension-Name": LAMBDA_EXTENSION_NAME,
    }
    payload = {
        "events": ["INVOKE", "SHUTDOWN"],
    }
    response = requests.post(  # pylint: disable=missing-timeout
        url=f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/register",
        json=payload,
        headers=headers,
    )
    ext_id = response.headers["Lambda-Extension-Identifier"]
    print(f"[{LAMBDA_EXTENSION_NAME}] Registered with ID: {ext_id}", flush=True)

    return ext_id


def process_events(ext_id):
    """Function to listens to streams from the log API and sends to extension.

    Args:
        ext_id (_type_): Extension id.
    """
    headers = {"Lambda-Extension-Identifier": ext_id}
    while True:
        print(f"[{LAMBDA_EXTENSION_NAME}] Waiting for event...", flush=True)
        response = requests.get(
            url=f"http://{os.environ['AWS_LAMBDA_RUNTIME_API']}/2020-01-01/extension/event/next",
            headers=headers,
            timeout=None,
        )
        event = json.loads(response.text)
        if event["eventType"] == "SHUTDOWN":
            # execute_custom_shutdown(event)
            print(f"[{LAMBDA_EXTENSION_NAME}] Gracefully exiting.", flush=True)
            sys.exit(0)
        else:
            execute_custom_processing(event)


def main():
    """Organizes the logic the extension"""

    # handle signals
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # start http server for IPC
    subscribe_to_ipc()

    # execute extensions logic
    extension_id = register_extension()
    process_events(extension_id)


if __name__ == "__main__":
    main()
