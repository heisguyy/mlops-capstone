.SILENT: quality-checks unit-test integration-test build setup check-infrastructure deploy-prefect

quality-checks:
	black .
	isort .
	pylint --recursive=y .

unit-test: quality-checks
	pytest .

integration-test: unit-test
	WANDB_KEY=${WANDB_KEY} integration_test/integration.sh

check-infrastructure:
	cd infrastructure; \
	terraform init; \
	terraform plan -var-file=vars/prod.tfvars

deploy-prefect:
	cd pipeline; \
	python train.py \
	prefect work-queue preview default --hours 100000 \
	prefect agent start --work-queue "default"

setup:
	pipenv install
	pipenv shell
	pre-commit install
