from django.contrib import admin

# Register your models here.
from .models import Notes, Lable

admin.site.register(Notes)
admin.site.register(Lable)
# admin.site.register(Colabrator)
