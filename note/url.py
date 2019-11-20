from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from note import views
from fundoo.swagger_view import schema_view

urlpatterns = [

    path("notes/", views.NoteCreate.as_view(), name="notes"),
    path("note/<note_id>", views.NoteUpdate.as_view(), name="note_update"),
    path("noteshare", views.NoteShare.as_view(), name="note_share"),
    path("label/<label_id>", views.LabelsUpdate.as_view(), name="label_update"),
    path("label", views.LabelsCreate.as_view(), name="label_get"),
    path("archive", views.Archive.as_view(), name="archive"),
    # path("label", views.Labels/Create.as_view()),
    path("trash", views.Trash.as_view(), name="trash"),
    path("reminder", views.Reminders.as_view(), name="reminder"),
    # path("lazy", views.LazyLoading.as_view(), name="lazy"),
    path("celery", views.Celery.as_view(), name="celery"),
    path("search", views.SearchEngine.as_view(), name="search"),

]
