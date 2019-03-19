FROM python:3.6.2-slim

ENV REDIS_HOST localhost
ENV REDIS_PORT 6379
ENV RABBITMQ_HOST localhost
ENV RABBITMQ_PORT 5672

RUN apt-get update && apt-get -y install gcc && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /crawlers/requirements.txt
RUN pip install -r /crawlers/requirements.txt
ADD src/crawlers/ceuta /ceuta

CMD cd /ceuta && scrapy crawl elfarodeceuta
