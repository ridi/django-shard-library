.PHONY: dist

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Install
install-dev:
	@pip3.6 install -r requirements/development.txt

# Test
lint:
	python $(shell which pylint) ./shard ./tests --rcfile=.pylintrc && flake8

test:
	python runtests.py

# Release
dist:
	rm -rf ./dist
	python setup.py sdist

pypi-upload:
	twine upload dist/*

pypi-test-upload:
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: dist pypi-upload
