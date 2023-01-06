FROM python:3.10
EXPOSE 5001
WORKDIR /code/app
COPY ./app /code/app

RUN apt-get update \
    && apt-get -y install kafkacat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./entrypoint.sh .
RUN chmod +x /code/app/entrypoint.sh
ENTRYPOINT ["sh", "/code/app/entrypoint.sh"]
