from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from note import views
from fundoo.swagger_view import schema_view


urlpatterns = [


    path("notes/",views.Create.as_view()),
    path("note/<note_id>",views.Update.as_view(), name="note_view"),
    path("noteshare", views.NoteShare.as_view()),
    path("label/<label_id>", views.LabelsUpdate.as_view()),
    path("label", views.LabelsCreate.as_view()),
    path("archive", views.Archive.as_view()),
    # path("label", views.Labels/Create.as_view()),
    path("trash", views.Trash.as_view()),
    path("reminder", views.Reminders.as_view()),
    path("lazy", views.LazyLoading.as_view()),
    path("sns", views.Sns.as_view()),
]