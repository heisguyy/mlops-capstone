from prefect import flow, task
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.task_runners import SequentialTaskRunner


@task
def get_logs():
    """
    _summary_
    """


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
