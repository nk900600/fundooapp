# import pika
# import requests
#
# from fundoo.settings import AUTH_ENDPOINT
#
# #
# # def message_broker(body):
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()
#
# # channel.queue_declare(queue='hello')
# # headers.put("x-delay", 5000)
# body="hi"
# channel.basic_publish(exchange='', routing_key='hello', body=body)
# print(" [x] Sent 'Hello World!'")
# connection.close()

#
#
# import smtplib
# from email.mime.text import MIMEText
#
# me = "me@example.com"
# you = "nk90600@gmail.com"
#
# msg = MIMEText("Hello world!")
# msg['From'] = me
# msg['To'] = you
# msg['Subject'] = 'Greetings'
#
# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.login("guest", "guest")
# s.sendmail(me, [you], msg.as_string())
# s.quit()

import smtplib

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login("nk90600@gmail.com", "pankaj007")

# message to be sent
message = "Message_you_need_to_send"

# sending the mail
s.sendmail("nk90600@gmail.com", "nk90600@gmail.com", message)

# terminating the session
s.quit()