House Price Prediction System
==============================
Problem statement
----------------
This project aims at building an end to end machine learning system to predict the prices of houses in America (14 States).  People are usually faced with the problem of valuing a house fairly whether it's a prospective buyer or a seller. They want to get a fair compenstaion for whatever they are sacrificing. The government can also accurately value the property of a citizen thereby preventing any attempt at fraud. A [kaggle dataset](https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset) that is updated weekly was used to train the model used in this system. The features from this datasetb used to build the model where number of beds, number of bathrooms, size of land on which the property sits, zip code of area, size of the house and a derived variable from state and city, location. The system would be deployed as API, so anyone can integrate it into their product or build a product around it.

------------
<!--
docker run --detach \
-e WANDB_KEY=202ada5746d12050a9ba2b9834945a9c1c973d08 \
-e MODEL_MONITOR_S3_BUCKET=testing \
-e IS_TEST=true \
-p 8000:8080 \
-v ~/.aws:/root/.aws:ro  \
mlops-capstone:latest -->


Project Structure
------------
    ├── .github/workflows       <- CI/CD and automation files.
    │   ├── deploy.yml          <- Github action for continuous deployment (CD).
    │   └── integration.yml     <- Github action for continuous integration tests (CI).
    │── .vscode/settings.json   <- Visual studio code IDE config files.
    ├── artifacts               <- Trained and serialized models, vectorizers, encoders, tokenizers, etc.
    ├── data                    <- Data used for the project
    ├── experiments/            <- Jupyter notebooks. Naming convention is a number (for ordering)
    │                              and a short `-` delimited description, e.g.
    │                              `1.0-initial-data-exploration`.
    ├── infrastructure          <- IaC files.
    │   ├── modules/            <- Modules of various components of the deployment infrastructure.
    │   ├── vars/               <- Defined variables for stages of the development lifecycle.
    │   ├── Dockerfile          <- Dummy dockerfile for AWS lambda initialization.
    │   ├── main.tf             <- Terraform declaration of backend and infrastructure.
    │   ├── output.tf           <- Declaration of terraform outputs.
    │   └── variables.tf        <- Terraform initialization of variables for the infrastructure.
    ├── integration_test        <- Integration tests.
    │   ├── docker-compose.yml  <- Docker compose to startup localstack and our API container.
    │   ├── integration.py      <- Scripts to query the infrastructure and verify outputs.
    │   └── integration.sh      <- Shell script to start build, start infrastructure and test it.
    ├── pipeline                <- Code for continous training and monitoring.
    │   ├── __init__.py         <- Makes pipeline a Python module.
    │   ├── monitoring.py       <- Script for batch monitoring.
    │   └── train.py            <- Script for continuous training.
    ├── src                     <- Source code for use in this project.
    │   ├── extensions/         <- Files for lambda extension used to log metrics to s3 bucket.
    │   ├── __init__.py         <- Makes src a Python module
    │   ├── main.py             <- Contains API codes.
    │   ├── monitor.py          <- Contains help functions send metrics to lambda extension.
    │   └── schema.py           <- Contains codes for data validation of both API inputs and Output.
    ├── tests                   <- Tests codes to ensure quality of codes.
    ├── .env                    <- Contains environmental variables like app secrets. This file should not
    │                              be committed or pushed.
    ├── .gitignore              <- List of files to avoid committing/pushing to the local and remote git repo.
    ├── .pre-commit-config.yaml <- Configurations of checks to run before a commit is accepted.
    ├── Dockerfile              <- Blueprint for building docker container.
    ├── LICENSE                 <- Permissions for the public on the use/distribution of the repo/project.
    ├── Makefile                <- Makefile with commands like `make setup`.
    ├── Pipfile                 <- Contains list of python packages used in this project.
    ├── Pipfile.lock            <- Encrypted files list of python package.
    ├── pyproject.toml          <- Configuration settings for black, isort, pylint and pytests.
    └── README.md               <- The top-level README for developers/users using this project.

--------
Stack
--------
Weights & Biases - Experimentation and Model Registry
Prefect and Prefect Cloud - Workflow orchestration
AWS(Lambda, S3, ECR and API gateway) and FastAPI- Cloud Provider and Web framework.
Terraform - IaC
Pytest - Unit tests
Black and Isort - Formatter
pre-commit: pre commit checks
Makefile: Code Automation tool
Github Action: CI/CD
Docker, Docker compose - Integration test.

--------
Steps to run the project
--------
To have run this project you need to have python and pipenv installed on your system.

Step 1: Clone the repo and move into it.
```
git clone https://github.com/heisguyy/mlops-capstone.git && cd mlops-capstone
```
Step 2: Setup environment and pre-commit
```
make setup
```
Step 3: Create a [wandb](https://wandb.ai/site) account if you don't have, create a project called `capstone-mlops` and get your API Key for your weights and bias account and export it to you terminal. You can add this command to `~/.bashrc` to add it permanently or just rerun the command everytime if you close your terminal and you want to continue testing.
```
export WANDB_KEY=<your-key>
```
Step 4: Create a kaggle account if you do not have one, get your kaggle API token. Download it, create a directory named `.kaggle` in your home directory and add the json file downloaded when you created the API token
Step 5: Download the dataset into the `data` folder.
```
kaggle datasets download -d ahmedshahriarsakib/usa-real-estate-dataset -p data/ --unzip
```
Step 6: Go to the `experiments` folder, open the jupyter notebook files and run them according to their numbering.
Step 7: Run all quality checks, unit test and integration test.
```
make integration-test
```
Step 8: Check terraform infrastructure.
```
make check-infrastructure
```
Step 9: Create an prefect cloud account, create an API key and a workspace. Configure your API key and workspace locally.
```
prefect cloud login -k <your-api-key>
```
you will be prompted to choose the workspace you created and a profile name.
Step 10: Deploy flow to cloud.
```
make deploy-prefect
```


N.B: Prefect pipeline for monitoring is not done and I also have a bug in the deployment causing the API gateway to not respond to requests. I will be working on this after this submission but you won't see it because you will be required reviewing the last commit before my submission.

--------

<p><small>This project uses <a target="_blank" href="https://github.com/heisguyy/cookiecutter-data-science">Olajide Oluwatosin's modification</a> of the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a> with a little more modifications.
