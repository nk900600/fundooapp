
from django.db import models




class SocialLogin(models.Model):
    unique_id = models.CharField(max_length=500)
    provider = models.CharField("service provider", max_length=500)
    username = models.CharField(max_length=500)
    full_name = models.CharField(max_length=500)
    EXTRA_PARAMS = models.TextField("extra params", max_length=1000)

    def __str__(self):
        return self.provider+" " + self.username
