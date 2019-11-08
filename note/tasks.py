# import redis
from celery import Celery
from celery.schedules import crontab
# from django.core.mail.message import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from tasks import *
import smtplib

# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from requests import request
#
# from fundoo.settings import BROKER
# red = redis.StrictRedis(host="localhost", db=0, port=6379)
# from lib.redis import red

app = Celery('hello', broker="amqp://guest@localhost//")

app.conf.beat_schedule = {
    'test-task': {
        'task': 'tasks.email',
        'schedule': crontab(),
    },
}

@app.task
def email():
    print('9')


    #
    # subject, from_email, to = 'hello', 'nk90600@gmail.com', red.get("recipientemail").decode('utf-8')
    # text_content = 'This is an important message.'
    # mail_message = render_to_string('user/email_validation.html', {
    #     'user': username,
    #     'domain': get_current_site(request).domain,
    #
    # })
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(mail_message, "text/html")
    # msg.send()
    #
    #
    # message = "Message_you_need_to_send"
    #
    # # sending the mail
    # s.sendmail(red.get("host-email").decode('utf-8'), red.get("recipientemail").decode('utf-8'), message)
    #
    # # terminating the session
    # s.quit()



