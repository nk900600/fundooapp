



from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from socialapp import views
from fundoo.swagger_view import schema_view

urlpatterns = [

    path("auth/", views.Oauth.as_view(), name="Oauth"),
    path("github/", views.Github.as_view(), name="github"),
]
