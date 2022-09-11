House prices
==============================

Predicting the price of houses in 14 states in the United States of America.

docker run --detach \
-e WANDB_KEY=202ada5746d12050a9ba2b9834945a9c1c973d08 \
-e MODEL_MONITOR_S3_BUCKET=testing \
-e IS_TEST=true \
-p 8000:8080 \
--add-host=host.docker.internal:127.0.0.1 \
mlops-capstone:monitoring



Project Structure
------------
    ├── .github/workflows       <- CI/CD and automation files.
    │   ├── deploy.yml          <- Github action for continuous deployment (CD).
    │   └── integration.yml     <- Github action for continuous integration tests (CI).
    │── .vscode/settings.json   <- Visual studio code IDE config files.
    ├── artifacts               <- Trained and serialized models, vectorizers, encoders, tokenizers, etc.
    ├── data                    <- Data used for the project
    ├── experiments             <- Jupyter notebooks. Naming convention is a number (for ordering)
    │                              and a short `-` delimited description, e.g.
    │                              `1.0-initial-data-exploration`.
    ├── infrastructure          <- IaC files.
    │   ├── modules/            <- Modules of various components of the deployment infrastructure.
    │   ├── vars/               <- Defined variables for stages of the development lifecycle.
    │   ├── main.tf             <- Terraform declaration of backend and infrastructure.
    │   └── variables.tf        <- Terraform initialization of variables for the infrastructure.
    ├── src                     <- Source code for use in this project.
    │   ├── __init__.py         <- Makes src a Python module
    │   ├── main.py             <- Scripts for API.
    │   └── Dockerfile          <- Blueprint for building docker container.
    ├── tests                   <- Tests codes to ensure quality of codes.
    │   ├── integration/        <- Codes to ensure changes haven't broken any essential feature.
    │   └── unit/               <- Codes to ensure that each function/unit is performing as expected.
    ├── .env                    <- Contains environmental variables like app secrets. This file should not
    │                              be committed or pushed.
    ├── .gitignore              <- List of files to avoid committing/pushing to the local and remote git repo.
    ├── .pre-commit-config.yaml <- Configurations of checks to run before a commit is accepted.
    ├── LICENSE                 <- Permissions for the public on the use/distribution of the repo/project.
    ├── Makefile                <- Makefile with commands like `make requirements`.
    ├── README.md               <- The top-level README for developers using this project.
    ├── pyproject.toml          <- Makefile with commands like `make data` or `make train`
    └── requirements.txt        <- List of libraries/packages and their versions required for the project.


--------

<p><small>This project uses <a target="_blank" href="https://github.com/heisguyy/cookiecutter-data-science">Olajide Oluwatosin's modification</a> of the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>.
