import os
from pickle import load
from typing import Optional

import numpy as np
import wandb
from catboost import Pool

from .monitor import (  # pylint: disable=unused-import,import-error
    log_inputs_for,
    log_outputs_for,
)


def download():
    """
    Download model and encoder.
    """
    # pylint: disable=global-variable-undefined

    wandb.login(key=os.getenv("WANDB_KEY"))

    api = wandb.Api()
    model_path = api.artifact(
        "heisguyy/capstone-mlops/capstone-model:latest"
    ).download(root="/tmp/")
    with open(f"{model_path}/2022-08-15.cbm", "rb") as model_file:
        model = load(model_file)
    encoder_path = api.artifact(
        "heisguyy/capstone-mlops/capstone-encoder:latest"
    ).download(root="/tmp/")
    with open(f"{encoder_path}/2022-08-15.bin", "rb") as encoder_file:
        encoder = load(encoder_file)

    return model, encoder


def lambda_handler(
    event, context: Optional[str] = None
):  # pylint: disable=unused-argument

    """Lambda function to make prediction

    Returns
        price (InferenceOutput): returns price in the format of int defined by the
        pydantic class InferenceOutput
    """

    model, encoder = download()

    if context:
        log_inputs_for("1234", [event])
    location = (
        "_".join(event["state"].lower().split())
        + "-"
        + "_".join(event["city"].lower().split())
    )
    location = encoder.transform(np.array([location])).item()
    price = model.predict(
        Pool(
            data=[
                [
                    event["num_of_bed"],
                    event["num_of_bath"],
                    event["acre_lot"],
                    event["zip_code"],
                    event["house_size"],
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
    if context:
        log_outputs_for("1234", [{"price": price.item()}])

    return {"price": price.item()}
