



from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from note import views
from services.swagger_view import schema_view

urlpatterns = [


    path("note/",views.Create),

]
