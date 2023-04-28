FROM python:3.8

RUN apt-get update && apt-get install -y \
    apt-utils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
RUN mkdir /src
WORKDIR /src

COPY poetry.lock pyproject.toml /src/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi 

COPY roughnator /src/roughnator
COPY data /src/data

EXPOSE 8000
ENTRYPOINT ["uvicorn", "roughnator.main:app", "--host", "0.0.0.0", "--port", "8000"]
