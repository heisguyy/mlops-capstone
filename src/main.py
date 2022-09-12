import os
from pickle import load

import numpy as np
import wandb
from catboost import Pool
from fastapi import FastAPI, status
from mangum import Mangum

from .monitor import (  # pylint: disable=unused-import,import-error
    log_inputs_for,
    log_outputs_for,
)
from .schema import InferenceInput, InferenceOutput  # pylint: disable=import-error

wandb.login(key=os.getenv("WANDB_KEY"))
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

    api = wandb.Api()
    model_path = api.artifact(
        "heisguyy/capstone-mlops/capstone-model:latest"
    ).download()
    with open(f"{model_path}/2022-08-15.cbm", "rb") as model_file:
        MODEL = load(model_file)
    encoder_path = api.artifact(
        "heisguyy/capstone-mlops/capstone-encoder:latest"
    ).download()
    with open(f"{encoder_path}/2022-08-15.bin", "rb") as encoder_file:
        ENCODER = load(encoder_file)


@app.on_event("shutdown")
def shutdown():
    """
    Instructions to execute on shutdown.
    """
    wandb.finish()


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
        pydantic class InferenceOutput
    """
    log_inputs_for("1234", [body.dict()])
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

    log_outputs_for("1234", [{"price": price.item()}])

    return {"price": price.item()}


handler = Mangum(app=app)
