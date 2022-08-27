.SILENT: quality-checks unit-test integration-test build publish test

quality-checks:
	black .
	isort .
	pylint --recursive=y .

unit-test: quality-checks
	pytest tests/unit/

integration-test: unit-test
	bash

build: integration-test
	docker build -t

publish: build

test:
	echo "I am testing\n"
