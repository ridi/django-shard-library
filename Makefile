.PHONY:

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# pre-processing
lint:
	@python3.6 $(shell which pylint) ./shard ./tests --rcfile=.pylintrc && flake8

test:
	@python3.6 runtests.py

