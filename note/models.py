from django.contrib.auth.models import User
from django.db import models



class Lable(models.Model):
    # notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='label_user',default="admin")

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=500)
    note = models.CharField(max_length=500, )
    image = models.ImageField(max_length=500, blank=True, null=True)
    archive = models.BooleanField("is_archived", default=False)
    delete_note = models.BooleanField("delete_note", default=False)
    label = models.ManyToManyField(Lable, blank=True)
    colaborator = models.ManyToManyField(User, related_name='collaborator', blank=True)
    copy = models.BooleanField("make a copy", default=False)
    checkbox = models.BooleanField("check box", default=False)
    pin = models.BooleanField(default=False)
    # trash = models.BooleanField(default=False)

    def __str__(self):
        return self.note





# class Colabrator(models.Model):
#     # notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
#     name = models.CharField(max_length=500)
