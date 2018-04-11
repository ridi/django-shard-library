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

# Prepare to test
run-test-db:
	make up-test-db
	sh docker/wait_for_it.sh 'mysqladmin ping -h 127.0.0.1 -u root -proot' 'make initialize'

stop-test-db:
	@docker-compose -f docker/docker-compose-test-db.yml down

up-test-db:
	@docker-compose -f docker/docker-compose-test-db.yml up -d

initialize:
	make create-database
	make migration

create-database:
	@mysql -h 127.0.0.1 -u root -p < docker/create_database.sql

migration:
	@python3.6 runcommand.py migrate


# Release
dist:
	rm -rf ./dist
	python setup.py sdist

pypi-upload:
	twine upload dist/*

pypi-test-upload:
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: dist pypi-upload
