# pylint: disable=missing-timeout
from pprint import pprint

import requests
from deepdiff import DeepDiff

URL = "http://localhost:9000/2015-03-31/functions/function/invocations"
expected_response = {"price": 496737.5}

response = requests.post(
    URL,
    json={
        "num_of_bed": 2,
        "num_of_bath": 3,
        "acre_lot": 0.12,
        "zip_code": 795,
        "house_size": 2520,
        "state": "Puerto Rico",
        "city": "Adjuntas",
    },
).json()

pprint(response)


diff = DeepDiff(
    expected_response["price"],
    response["price"],
    significant_digits=0,
)
print("diff")
pprint(diff)

assert "values_changed" not in diff
