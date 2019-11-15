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

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Registration):
            return self.name == other.name
        return "cannot equalize different classes"

    def __repr__(self):
        return "Note({!r},{!r},{!r})".format(self.name, self.username, self.email)


    class Meta:
        """
        name is given which will be displayed in admin page
        """
        verbose_name = 'user detail'
        verbose_name_plural = 'user details'
