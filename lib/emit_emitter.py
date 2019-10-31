from django.core.mail import EmailMultiAlternatives
from pyee import BaseEventEmitter

from fundoo.settings import EMAIL_HOST_USER

ee = BaseEventEmitter()


@ee.on('send_email')
def send_email(recipientemail, mail_message):
    msg = EmailMultiAlternatives(subject="password reset link", from_email=EMAIL_HOST_USER,
                                 to=[recipientemail], body=mail_message)
    msg.attach_alternative(mail_message, "text/html")
    msg.send()
