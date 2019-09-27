from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=500)
    Note = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    archive = models.BooleanField("is_archived", default=False)
    delete_note = models.BooleanField("delete_note", default=False)
    label = models.CharField(max_length=500)
    colabrator = models.CharField(max_length=500)
    copy = models.BooleanField("make a copy", default=False)
    checkbox = models.BooleanField("check box", default=False)
    pin = models.BooleanField(default=False)
    trash = models.BooleanField(default=False)

    def __str__(self):
        return self.Title


class Lable(models.Model):
    notes = models.ForeignKey(Notes,on_delete=models.CASCADE)
    label = models.CharField(max_length=500)