from django.contrib.auth.models import User, AbstractUser
from django.db import models


# class CustomUser(AbstractUser):
#     new_field = models.CharField(max_length=100, blank=True)


class Label(models.Model):
    name = models.CharField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='label_user', default="admin")

    def __str__(self):
        return self.name


# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=500, blank=True)
    note = models.CharField(max_length=500, )
    image = models.ImageField(max_length=500, blank=True, null=True, upload_to="image")
    archive = models.BooleanField("is_archived", default=False)
    delete_note = models.BooleanField("delete_note", default=False)
    label = models.ManyToManyField(Label, related_name="label", blank=True)
    coll = models.ManyToManyField(User, related_name='coll', blank=True)
    copy = models.BooleanField("make a copy", default=False)
    checkbox = models.BooleanField("check box", default=False)
    pin = models.BooleanField(default=False)
    url = models.URLField(blank=True)
    reminder = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.note
