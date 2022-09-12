# pylint: disable=import-error
from fastapi.testclient import TestClient

from src.lambda_function import app


def test_root_endpoint():
    """
    Test the root endpoint of the API
    """
    with TestClient(app) as api:
        response = api.get(
            "/",
        )
        assert response.json() == {
            "Message": "Welcome to my capstone project for the mlops zoomcamp."
        }


# def test_predict_data():
#     """
#     Test the predict endpoint of the API
#     """
#     with TestClient(app) as api:
#         response = api.post(
#             "/predict",
#             json={
#                 "num_of_bed": 2,
#                 "num_of_bath": 3,
#                 "acre_lot": 0.12,
#                 "zip_code": 795,
#                 "house_size": 2520,
#                 "state": "Puerto Rico",
#                 "city": "Adjuntas",
#             },
#         )
#         assert response.status_code == 200
#         assert response.json() == {"price": 496737.5880460376}
