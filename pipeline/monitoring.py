# pylint: skip-file
from prefect import flow, task
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner
from prefect_aws import AwsCredentials
from prefect_aws.s3 import s3_download, s3_list_objects


@task
def get_logs():
    """
    _summary_
    """
    aws_credentials = AwsCredentials(
        aws_access_key_id="access_key_id", aws_secret_access_key="secret_access_key"
    )
    objects = s3_list_objects(bucket="data_bucket", aws_credentials=aws_credentials)
    for object in objects:
        data = s3_download(bucket="bucket", key="key", aws_credentials=aws_credentials)


@task
def calculate_drift():
    """
    _summary_
    """


@task
def save_report():
    """
    _summary_
    """


@flow(task_runner=SequentialTaskRunner())
def main():
    """
    _summary_
    """
    get_logs()
    calculate_drift()
    save_report()


deployment = Deployment.build_from_flow(
    flow=main,
    name="monitoring",
    version="0.0.1",
    schedule=CronSchedule(cron="0 2 * * *"),
    tags=["mlops-capstone"],
)
deployment.apply()
