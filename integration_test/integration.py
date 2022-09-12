# pylint: disable=missing-timeout
import json
from pprint import pprint

import requests
from deepdiff import DeepDiff

URL = "http://localhost:9000/2015-03-31/functions/function/invocations"
expected_response = {
    "body": '{"price":496737.5}',
    "headers": {"content-length": "27", "content-type": "application/json"},
    "isBase64Encoded": False,
    "multiValueHeaders": {},
    "statusCode": 200,
}

load = json.dumps(
    {
        "num_of_bed": 2,
        "num_of_bath": 3,
        "acre_lot": 0.12,
        "zip_code": 795,
        "house_size": 2520,
        "state": "Puerto Rico",
        "city": "Adjuntas",
    }
)

response = requests.post(
    URL,
    json={
        "resource": "/predict",
        "path": "/predict",
        "httpMethod": "POST",
        "requestContext": {},
        "body": load,
    },
).json()


expected_root_response = {
    "body": '{"Message":"Welcome to my capstone project for the mlops zoomcamp."}',
    "headers": {"content-length": "68", "content-type": "application/json"},
    "isBase64Encoded": False,
    "multiValueHeaders": {},
    "statusCode": 200,
}

root_response = requests.post(
    URL,
    json={
        "resource": "/",
        "path": "/",
        "httpMethod": "GET",
        "requestContext": {},
        "body": {},
    },
).json()

diff = DeepDiff(
    json.loads(response["body"])["price"],
    json.loads(expected_response["body"])["price"],
    significant_digits=0,
)
print("diff")
pprint(diff)

assert "values_changed" not in diff

root_diff = DeepDiff(root_response, expected_root_response)
print("\nRoot diff")
pprint(root_diff)

assert "values_changed" not in root_diff
