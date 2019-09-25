from django.contrib import admin

# Register your models here.
from login.models import Registration, LoggedUser

admin.site.register(LoggedUser)
@admin.register(Registration)
class Registrationadmin(admin.ModelAdmin):
    list_display = ('name','username','email','password')