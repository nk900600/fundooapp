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
