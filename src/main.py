from pickle import load

import numpy as np
from catboost import Pool
from fastapi import FastAPI, status
from mangum import Mangum

from .monitor import log_inputs_for, log_outputs_for  # pylint: disable=unused-import
from .schema import InferenceInput, InferenceOutput

app = FastAPI(
    title="House Predictor API",
    description="This API predicts prices of houses in the United States of America",
    version="0.0.1",  # update this version to 1.0.0 one first release.
    redoc_url=None,
)


@app.on_event("startup")
def startup():
    """
    Instructions to execute on startup.
    """
    # pylint: disable=global-variable-undefined

    global MODEL, ENCODER

    with open("artifacts/2022-08-15.cbm", "rb") as pickle_file:
        MODEL = load(pickle_file)
    with open("artifacts/2022-08-15.bin", "rb") as pickle_file:
        ENCODER = load(pickle_file)


@app.get("/")
def home() -> dict:
    # pylint: disable=missing-function-docstring
    return {"Message": "Welcome to my capstone project for the mlops zoomcamp."}


@app.post(
    "/predict",
    status_code=status.HTTP_200_OK,
    tags=["Prediction"],
    response_model=InferenceOutput,
)
def predict_data(body: InferenceInput):

    """Prediction endpoint

    Returns
        price (InferenceOutput): returns price in the format of int defined by the
        pydantic class InteferenceOutput
    """

    # log_inputs_for(body)
    location = (
        "_".join(body.state.lower().split()) + "-" + "_".join(body.city.lower().split())
    )
    location = ENCODER.transform(np.array([location])).item()
    price = MODEL.predict(
        Pool(
            data=[
                [
                    body.num_of_bed,
                    body.num_of_bath,
                    body.acre_lot,
                    body.zip_code,
                    body.house_size,
                    location,
                ]
            ],
            feature_names=[
                "bed",
                "bath",
                "acre_lot",
                "zip_code",
                "house_size",
                "location",
            ],
        )
    )

    # log_outputs_for(price)

    return {"price": price.item()}


handler = Mangum(app=app)
