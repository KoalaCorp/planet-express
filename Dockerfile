FROM python:3.6.2-slim

ENV REDIS_HOST redis
ENV REDIS_PORT 6379
ENV RABBITMQ_HOST rabbitmq
ENV RABBITMQ_PORT 5672
ENV RABBITMQ_QUEUE items

RUN apt-get update && apt-get -y install gcc && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /crawlers/requirements.txt
RUN pip install -r /crawlers/requirements.txt
ADD src/crawlers/ceuta /ceuta
