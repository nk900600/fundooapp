import pika
import requests

from fundoo.settings import AUTH_ENDPOINT
from services.token import token_validation

def message_broker(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    data = {
        "username": "admin",
        "password": "admin"
    }

    channel.basic_publish(exchange='', routing_key='hello', body=body)
    print(" [x] Sent 'Hello World!'")
    connection.close()

