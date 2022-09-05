FROM python:3.7.13-slim-buster

# set working dir in container
WORKDIR /bot

USER root

RUN python -m pip install --upgrade pip
# installing prework for psycopg2 package
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# install dependencies
COPY requirements.txt /bot
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY ./bot_framework/ ./bot_framework
COPY ./tests/ ./tests
COPY ./env/ ./env
COPY ./sql_files/ ./sql_files

COPY config.env ./config.env
COPY ./remote_server/api_frame/api.py ./api.py


CMD [ "python", "./api.py" ]
