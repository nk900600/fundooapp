import pika
import requests

from fundoo.settings import AUTH_ENDPOINT

#
# def message_broker(body):
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body="hkibhb")
print(" [x] Sent 'Hello World!'")
connection.close()

