from django.contrib.auth.models import User, AbstractUser
from django.db import models

# class Labels(AbstractUser):
#     label= models.CharField(unique=True,max_length=254 , blank=True)

class Label(models.Model):
    name = models.CharField(unique=True, max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='label_user', default="admin")
    #
    # @classmethod
    # def create(cls, name):
    #     lab = cls(name=name)
    #     # do something with the book
    #     return l

    def __str__(self):
        return self.name


# class collaborator(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Colabrator_user')
#     name = models.CharField(max_length=500)


# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=500,blank=True)
    note = models.CharField(max_length=500, )
    image = models.ImageField(max_length=500, blank=True, null=True, upload_to="image")
    archive = models.BooleanField("is_archived", default=False)
    delete_note = models.BooleanField("delete_note", default=False)
    label = models.ManyToManyField(Label, related_name="label", blank=True)#, blank=True, null=True) #, on_delete=models.CASCADE)
    coll = models.ManyToManyField(User, related_name='coll', blank=True)
    copy = models.BooleanField("make a copy", default=False)
    checkbox = models.BooleanField("check box", default=False)
    pin = models.BooleanField(default=False)
    url = models.URLField(blank=True)


    def __str__(self):
        return self.note
