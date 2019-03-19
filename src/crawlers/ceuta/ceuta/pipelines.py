# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pika


class CeutaPipeline(object):
    def process_item(self, item, spider):
        return item


class RabbitMQPipeline(object):
    def __init__(self, rabbitmq_host, rabbitmq_port, rabbitmq_queue):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_queue = rabbitmq_queue

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            rabbitmq_host=crawler.settings.get('RABBITMQ_HOST'),
            rabbitmq_port=crawler.settings.get('RABBITMQ_PORT'),
            rabbitmq_queue=crawler.settings.get('RABBITMQ_QUEUE', 'items')
        )

    def open_spider(self, spider):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitmq_host, self.rabbitmq_port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.rabbitmq_queue, durable=True)

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.rabbitmq_queue,
            body=json.dumps(item.__dict__['_values']),
            properties=pika.BasicProperties(delivery_mode=2))
        return item
