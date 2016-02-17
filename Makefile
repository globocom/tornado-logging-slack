TESTS_FILE=tests.py
MODULE_DIR=tornado_logging_slack/

.PHONY: all setup clean flake8 coverage
all: clean setup test

setup:
	@pip install -Ue .\[tests\]

clean:
	find . -name "*.pyc" -exec rm '{}' ';'

flake8:
	flake8 ${MODULE_DIR}
	flake8 ${TESTS_FILE}

upload:
	python ./setup.py sdist upload -r pypi

test:
	@coverage run --branch --source=${MODULE_DIR} `which nosetests` -v --with-yanc ${TESTS_FILE}
	@$(MAKE) coverage
	@$(MAKE) flake8

coverage:
	@coverage report -m --fail-under=83
