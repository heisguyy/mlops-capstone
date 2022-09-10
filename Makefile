.SILENT: quality-checks unit-test integration-test build publish test

quality-checks:
	black .
	isort .
	pylint --recursive=y .

unit-test: quality-checks
	pytest .

integration-test: unit-test
	bash .integration_test/integration

build: integration-test
	docker build --build-arg WANDB_KEY=202ada5746d12050a9ba2b9834945a9c1c973d08 -t mlops-capstone:latest .

publish: build
