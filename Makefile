.DEFAULT_GOAL := about
VERSION := $(shell cat async_metrics/__version__.py | cut -d'"' -f 2)

lint:
ifeq ($(SKIP_STYLE), )
	@echo "> running isort..."
	isort async_metrics/
	isort tests/
	isort setup.py
	@echo "> running black..."
	black async_metrics
	black tests
	black setup.py
endif
	@echo "> running flake8..."
	flake8 async_metrics
	flake8 tests
	@echo "> running mypy..."
	mypy async_metrics

tests:
	@echo "> unittest"
	python -m pytest -v --cov-report xml --cov-report term --cov=async_metrics tests

docs:
	@echo "> generate project documentation..."
	portray server

install-deps:
	@echo "> installing dependencies..."
	pip install -r requirements-dev.txt

tox:
	@echo "> running tox..."
	tox -r -p all

about:
	@echo "> async_metrics: $(VERSION)"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Execute tests."
	@echo "make ci           - Runs: [lint > tests]"
	@echo "make tox          - Runs tox."
	@echo "make docs         - Generate project documentation."
	@echo "make install-deps - Install development dependencies."
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

ci: lint tests
ifeq ($(TRAVIS_PULL_REQUEST), false)
	@echo "> download CI dependencies"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "> uploading report..."
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: ci


.PHONY: lint tests docs install-deps ci all
