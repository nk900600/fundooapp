from django.db import models
from django import forms
from django.contrib.auth.signals import user_logged_in, user_logged_out

class Registration(models.Model):

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    if name == "" or username == "" or email == "" or password == "":
        raise forms.ValidationError(" one of the above field is empty")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'user detail'
        verbose_name_plural = 'user details '


class LoggedUser(models.Model):
    username = models.CharField(max_length=30, primary_key=True)

    def __unicode__(self):
        return self.username


def login_user(sender, request, user, **kwargs):
    LoggedUser(username=user.username).save()


def logout_user(sender, request, user, **kwargs):
    try:
        u = LoggedUser.objects.get(pk=user.username)
        u.delete()
    except LoggedUser.DoesNotExist:
        pass


user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)