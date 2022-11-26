FROM python:3.10
WORKDIR /code/app
COPY ./app /code/app

RUN apt-get update \
    && apt-get -y install kafkacat\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip 
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY ./entrypoint.sh .
RUN chmod +x /code/app/entrypoint.sh

ENTRYPOINT ["sh", "/code/app/entrypoint.sh"]

