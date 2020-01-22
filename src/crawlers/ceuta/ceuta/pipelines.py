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
    def __init__(self, rabbitmq_host, rabbitmq_port, rabbitmq_queue,
                 rabbitmq_user, rabbitmq_password):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_queue = rabbitmq_queue
        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_password = rabbitmq_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            rabbitmq_host=crawler.settings.get('RABBITMQ_HOST'),
            rabbitmq_port=crawler.settings.get('RABBITMQ_PORT'),
            rabbitmq_queue=crawler.settings.get('RABBITMQ_QUEUE'),
            rabbitmq_user=crawler.settings.get('RABBITMQ_USER'),
            rabbitmq_password=crawler.settings.get('RABBITMQ_PASSWORD')
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        credentials = pika.PlainCredentials(self.rabbitmq_user,
                                            self.rabbitmq_password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.rabbitmq_host, self.rabbitmq_port,
                                      '/', credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.rabbitmq_queue, durable=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.rabbitmq_queue,
            body=json.dumps(item.__dict__['_values']),
            properties=pika.BasicProperties(delivery_mode=2))
        self.connection.close()
        return item
