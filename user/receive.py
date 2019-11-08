# import json
#
# import pika
#
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
# channel.exchange_declare(exchange='X')
#
#
# channel.queue_declare(queue='hello')
#
#
# def callback(ch, method, properties, body):
#     print(json.loads(body))
#     print(" [x] Received %r" % json.loads(body)[0])
#
#
# # channel.basic_consume(
# #     queue='hello', on_message_callback=callback, auto_ack=True)
# channel.basic_consume(
#     queue='celery', on_message_callback=callback, auto_ack=True)
#
# print(' [*] Waiting for messages. To exit press CTRL+C')
#
# channel.start_consuming()

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='X')
channel.queue_bind(exchange='X', queue='hello', routing_key='#')

channel.basic_publish(exchange='X',
    routing_key='nk90600@gmail.com',
    properties=pika.BasicProperties(
        content_type = 'text/plain',
        headers = {'Subject':'Greetings'}),
    body='Hello world!')
connection.close()