"""
this file is used for creating models
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

#


class Registration(models.Model):
    """
    This model is used for taking user information
    """
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    if name == "" or username == "" or email == "" or password == "":
        raise forms.ValidationError(" one of the above field is empty")

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        name is given which will be displayed in admin page
        """
        verbose_name = 'user detail'
        verbose_name_plural = 'user details '
