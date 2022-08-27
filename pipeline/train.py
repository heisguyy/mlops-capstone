import os
import warnings
from pickle import dump
from typing import Tuple
from datetime import date
from tempfile import TemporaryDirectory
import pandas as pd
from kaggle import api
import wandb
from wandb.catboost import WandbCallback
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from prefect import task, flow, get_run_logger
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner

warnings.filterwarnings("ignore")
os.environ["WANDB_SILENT"] = "true"

@task
def get_data() -> pd.DataFrame:
    """Gets data from kaggle.

    Returns:
        pd.DataFrame: Data to retrain model on.
    """
    with TemporaryDirectory() as tmpdirname:
        api.dataset_download_files(
            dataset="ahmedshahriarsakib/usa-real-estate-dataset",
            path=tmpdirname,
            unzip=True
        )
        data = pd.read_csv(tmpdirname+"/realtor-data.csv")

    return data

@task
def prepare_data(data: pd.DataFrame, current_date: str) -> Tuple[pd.DataFrame,pd.Series]:
    """Prepare data for retraining and log preprocessing artifacts to weights and biases.

    Args:
        data (pd.DataFrame): Updated dataset from kaggle.
        current_date (str): Current date of retraining.

    Returns:
        Tuple[pd.DataFrame,pd.Series]: features and labels respectively
    """
    logger = get_run_logger()

    data.drop_duplicates(inplace=True)
    logger.info("Duplicates dropped...")

    data.drop(["full_address","street","status","sold_date"],1,inplace=True)
    logger.info("Extra columns dropped...")

    data.dropna(inplace=True)
    logger.info("Empty values dropped...")

    rows_to_drop = data[data["price"]>50000000].index.to_list()
    rows_to_drop.extend(data[data.bed>40].index.to_list())
    rows_to_drop.extend(data[data.bath>50].index.to_list())
    rows_to_drop.extend(data[data.acre_lot>15000].index.to_list())
    rows_to_drop.extend(data[data.house_size>200000].index.to_list())
    data.drop(rows_to_drop,0,inplace=True)
    logger.info("Outliers dropped...")

    data.city = data.city.apply(lambda x: "_".join(x.lower().split()))
    data.state = data.state.apply(lambda x: "_".join(x.lower().split()))
    data["location"] = data.state + "-" + data.city
    data.drop(["city","state"],1,inplace=True)
    data.reset_index(inplace=True,drop=True)
    encoder = LabelEncoder()
    data["location"] = encoder.fit_transform(data["location"])
    logger.info("Categorical feature encoded dropped...")

    artifact = wandb.Artifact("capstone-encoder","preprocessor")
    with artifact.new_file(current_date+".bin", mode="wb") as file:
        dump(encoder,file)
    wandb.log_artifact(artifact)
    logger.info("Label encoder sent to weights and biases...")

    features = data.drop("price",1)
    labels = data.price


    return features,labels

@task
def train_model(features: pd.DataFrame, labels: pd.Series, current_date: str):
    """Trains model and logs the model to weights and biases.

    Args:
        features (pd.DataFrame): Features for prediction
        labels (pd.Series): Amount to be predicted
        current_date (str): current date
    """
    logger = get_run_logger()

    x_train, x_val, y_train, y_val = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=45,
        shuffle=True
    )
    logger.info("Dataset split...")

    wandb.config = {
        'learning_rate': 0.07632400095462799,
        'random_seed': 0,
        'depth': 6,
        'subsample': 0.800000011920929,
        'use_best_model': False,
        'silent': True,
        'eval_metric': "RMSE"
    }
    model = CatBoostRegressor(**wandb.config)
    model.fit(x_train,y_train,eval_set=(x_val,y_val),callbacks=[WandbCallback()])
    logger.info("Model trained...")

    y_preds = model.predict(x_val)
    error = mean_squared_error(y_val,y_preds,squared=False)
    wandb.summary["error"] = error
    logger.info("Error calculated and logged...")

    artifact = wandb.Artifact("capstone-model","model")
    with artifact.new_file(current_date+".cbm", mode="wb") as file:
        dump(model,file)
    wandb.log_artifact(artifact)
    logger.info("Model logged...")


@flow(task_runner=SequentialTaskRunner())
def main():
    """
    Runs previous function and definition of prefect flow
    """
    #pylint: disable=no-member

    today = f"{date.today()}"
    wandb.init(project="capstone-mlops", entity="heisguyy", name=today, tags=["Continual learning"])
    data = get_data().result()
    features, labels = prepare_data(data,today).result()
    train_model(features,labels,today)
    wandb.finish()


deployment = Deployment.build_from_flow(
    flow=main,
    name="continuous_learning",
    version="0.0.1",
    schedule= CronSchedule(cron="0 12 * * 0"),
    tags=["mlops-capstone"]
    )
deployment.apply()
