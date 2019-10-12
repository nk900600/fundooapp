from django.contrib import admin

# Register your models here.
from .models import Notes, Label

admin.site.register(Notes)
admin.site.register(Label)
# admin.site.register(Colabrator)
