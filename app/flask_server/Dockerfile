FROM python:3.8-buster

ARG ENV

ENV ENV=${ENV} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.13 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

RUN apt-get update \
    && apt-get -y install \
    cmake protobuf-compiler \
    libzbar0

# problem with this wkhtmltopdf!!
RUN apt-get -y install wkhtmltopdf

# Set the working directory to /app
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install $(test "$ENV" == production && echo "--no-dev") --no-ansi

# Creating folders, and files for a project:
COPY . /app

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]