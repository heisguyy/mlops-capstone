.SILENT: quality-checks unit-test integration-test build setup
WANDB_KEY=

quality-checks:
	black .
	isort .
	pylint --recursive=y .

unit-test: quality-checks
	pytest .

integration-test: unit-test
	WANDB_KEY=${WANDB_KEY} integration_test/integration.sh

build: integration-test
	docker build --build-arg -t mlops-capstone:latest .

setup:
	pipenv install --dev
	pre-commit install
