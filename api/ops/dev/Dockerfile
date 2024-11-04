FROM python:3.9-slim-bookworm
WORKDIR /api

COPY ./minitwitter/pyproject.toml ./minitwitter/poetry.lock /api/

RUN python -m pip install --upgrade pip==22.3.0 --ignore-installed \
    && pip install 'poetry==1.8.3' \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root \
    && rm -frv ~/.cache
