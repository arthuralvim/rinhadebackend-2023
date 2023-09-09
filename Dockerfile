FROM python:3.9-slim-buster

ENV \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:${PATH}"

RUN \
    apt-get update && apt-get install -y \
    curl \
    tini \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src/

RUN curl -sSL https://install.python-poetry.org | python -
COPY ./poetry.lock ./pyproject.toml /src/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root

COPY docker-entrypoint.sh initdb.py prestart.sh run.sh pytest.ini /src/
COPY app /src/app/

EXPOSE 80

ENTRYPOINT ["/usr/bin/tini", "--", "./docker-entrypoint.sh"]
CMD ["./run.sh"]
