# Use Python 3.13 slim image as base
FROM python:3.13-slim as python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.1 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# install postgres dependencies inside of Docker
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Set working directory
WORKDIR $PYSETUP_PATH

# Copy project files
COPY poetry.lock pyproject.toml ./

# Install project dependencies
RUN poetry install --no-dev

# quicker install as runtime deps are already installed
RUN poetry install

# Set app directory
WORKDIR /app

# Copy application code
COPY . /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]