import os
from pickle import dump
import warnings
warnings.filterwarnings("ignore")
from typing import Tuple
from datetime import date
import pandas as pd
import wandb
from wandb.catboost import WandbCallback


from prefect import task, flow, get_run_logger
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner


from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

wandb.login(key=os.getenv(key="WANDB_KEY"))

@task
def get_data() -> pd.DataFrame:
    data = pd.read_csv("")
    return data

@task
def prepare_data(data,current_date) -> Tuple[pd.DataFrame,pd.Series]:
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

    artifact = wandb.Artifact("capstone-artifacts","preprocessor")
    with artifact.new_file(current_date+".bin", mode="wb") as file:
        dump(encoder,file)
    wandb.log_artifact(artifact)
    logger.info("Label encoder sent to weights and biases...")

    features = data.drop("price",1)
    labels = data.price


    return features,labels

@task
def train_model(features,labels,current_date):
    logger = get_run_logger()

    x_train, x_val, y_train, y_val =train_test_split(features,labels,test_size=0.2,random_state=45,shuffle=True)
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
    y_preds = model.predict(x_val)
    error = mean_squared_error(y_val,y_preds,squared=False)
    wandb.summary["error"] = error

    artifact = wandb.Artifact("capstone-artifacts","model")
    with artifact.new_file(current_date+".bin", mode="wb") as file:
        dump(model,file)
    
    wandb.log_artifact(artifact)


@flow
def main():
    wandb.init(project="capstone-mlops", entity="heisguyy", name=date, tags=["Continual learning"])
    today = date.today()
    data = get_data()
    features, labels = prepare_data(data,today)
    train_model(features,labels,today)
    wandb.finish()

main()


# Deployment(
#     flow=main,
#     name="model_training",
#     schedule=CronSchedule(cron="0 9 15 * *"),
#     flow_runner=SubprocessFlowRunner()
# )