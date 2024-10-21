RESULTS ?= ./reports
CACHE_DIR ?= $(RESULTS)/.pytest_cache
POETRY_VIRTUALENVS_CREATE ?= false
EXTRAS ?= --all-extras

# do nothing by default
all:

test:
	RESULTS=$(RESULTS) pytest -ra -o cache_dir=$(CACHE_DIR)

install:
	poetry install $(EXTRAS) --no-interaction

.PHONY: all test
