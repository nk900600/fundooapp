from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from note import views
from services.swagger_view import schema_view

urlpatterns = [


    path("note/",views.Create.as_view()),
    path("note/<note_id>",views.Update.as_view()),
    path("noteshare", views.NoteShare.as_view()),
    path("label/<name>", views.LabelsUpdate.as_view()),
    path("label", views.LabelsCreate.as_view()),



]