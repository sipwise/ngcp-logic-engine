# DOCKER_NAME=ngcp-logic-engine-bookworm
FROM docker.mgm.sipwise.com/sipwise-bookworm:latest

# Important! Update this no-op ENV variable when this Dockerfile
# is updated with the current date. It will force refresh of all
# of the base images and things like `apt-get update` won't be using
# old cached versions when the Dockerfile is built.
ENV REFRESHED_AT 2024-06-04

RUN apt-get update && apt-get install --assume-yes \
  python3-poetry \
  git \
  && apt-get clean

ENV POETRY_VIRTUALENVS_CREATE=false
ENV RESULTS=/code/reports

# Get pip to download and install requirements:
ADD poetry.lock pyproject.toml /tmp/
RUN poetry install --no-root --with test --no-interaction --directory=/tmp

RUN git config --global --add safe.directory /code

RUN echo './t/testrunner' >>/root/.bash_history

WORKDIR /code/

################################################################################
# Instructions for usage
# ----------------------
# When you want to build the base image from scratch (jump to the next section if you don't want to build yourself!):
# % docker build --tag="ngcp-logic-engine-bookworm" -f t/Dockerfile .
# % docker run --rm -i -t -v $(pwd):/code:rw ngcp-logic-engine-bookworm:latest bash
#
# Use the existing docker image:
# % docker pull docker.mgm.sipwise.com/ngcp-logic-engine-bookworm
# % docker run --rm -i -t -v $(pwd):/code:rw docker.mgm.sipwise.com/ngcp-logic-engine-bookworm:latest bash
#
# Inside docker (the command is in history, just press UP button):
#   ./t/testrunner
#
# Run django inside docker:
# see README.md
################################################################################
