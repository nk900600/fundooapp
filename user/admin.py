from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from user.models import Registration


@admin.register(Registration)
class Registrationadmin(admin.ModelAdmin):
    list_display = ('name','username','email','password')