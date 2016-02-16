.PHONY: setup clean flake8 upload

setup:
	@pip install -Ue .\[tests\]

clean:
	find . -name "*.pyc" -exec rm '{}' ';'

flake8 static:
	flake8 tornado_logging_slack.py

upload:
	python ./setup.py sdist upload -r pypi
