FROM python:3.11

RUN apt-get update -y

RUN useradd -m python
USER python

ENV PATH=${PATH}:/home/python/.local/bin

RUN curl -sSL https://install.python-poetry.org | python3 - 

WORKDIR /app/prom-graf-usgs

COPY *.toml .
RUN poetry install

COPY *.py .

ENTRYPOINT poetry run python run.py