from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pyee import BaseEventEmitter

from fundoo import settings
from fundoo.settings import EMAIL_HOST_USER

ee = BaseEventEmitter()


@ee.on('send_email')
def send_email(recipientemail, mail_message):

    subject, from_email, to = 'greeting from fundoo ', settings.EMAIL_HOST, recipientemail
    msg = EmailMultiAlternatives(subject, mail_message, from_email, [to])
    msg.attach_alternative(mail_message, "text/html")
    msg.send()