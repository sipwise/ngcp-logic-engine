RESULTS ?= ./reports
CACHE_DIR ?= $(RESULTS)/.pytest_cache

# do nothing by default
all:

test:
	RESULTS=$(RESULTS) pytest -ra -o cache_dir=$(CACHE_DIR)

install:
	POETRY_VIRTUALENVS_CREATE=false \
	poetry install --all-extras --no-interaction

.PHONY: all test
