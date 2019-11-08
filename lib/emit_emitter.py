from django.core.mail import EmailMultiAlternatives
from pyee import BaseEventEmitter

from fundoo.settings import EMAIL_HOST_USER

ee = BaseEventEmitter()


@ee.on('send_email')
def send_email(recipientemail, mail_message):

    subject, from_email, to = 'hello', 'nk90600@gmail.com', recipientemail
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()