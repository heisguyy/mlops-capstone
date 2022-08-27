import json
from typing import List
from enum import Enum
import requests


LOGGING_ENDPOINT = 'http://127.0.0.1:2772'


class LogType(str, Enum):
    INPUTS = "INPUTS"
    RESULTS = "RESULTS"


def log_inputs_for(request_id: str, inputs: List):
    """Function to log input user sends to the lambda service.

    Args:
        request_id (str): Lambda request id for each request.
        results (List): Input requests sent to the lambda function.
    """
    # pylint: disable=missing-timeout

    requests.post(
        LOGGING_ENDPOINT,
        json={
            'type': LogType.INPUTS,
            'request_id': request_id,
            'inputs': json.dumps(inputs)
        }
    )


def log_outputs_for(request_id: str, results: List):
    """Function to log output/prediction of the model for model monitoring purposes.

    Args:
        request_id (str): Lambda request id for each request.
        results (List): prediction of the model which is the price of the property.
    """
    # pylint: disable=missing-timeout

    requests.post(
        LOGGING_ENDPOINT,
        json={
            'type': LogType.RESULTS,
            'request_id': request_id,
            'results': json.dumps(results)
        }
    )
