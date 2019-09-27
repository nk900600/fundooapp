from django.contrib import admin

# Register your models here.
from user.models import Registration


@admin.register(Registration)
class Registrationadmin(admin.ModelAdmin):
    list_display = ('name','username','email','password')