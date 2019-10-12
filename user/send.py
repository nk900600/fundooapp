# import pika
# import requests
#
# from fundoo.settings import AUTH_ENDPOINT
# from services.token import token_validation
#
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='hello')
# data = {
#     "username": "admin",
#     "password": "admin"
# }
#
# channel.basic_publish(exchange='', routing_key='hello', body="hello")
# print(" [x] Sent 'Hello World!'")
# connection.close()
#
#
