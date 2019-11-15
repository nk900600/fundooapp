
from rest_framework import serializers
from .models import Notes, Label
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from  .documents import NotesDocument

class NotesDocumentSerializer(DocumentSerializer):
    class Meta:
        document = NotesDocument
        fields = [
            'title'

        ]

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'note', 'label', 'url', 'is_archive', 'collaborators', 'image', 'reminder' ,'color']


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'note']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'note', 'label', 'url', 'is_archive', 'collaborators'
            ,"is_copied" ,'checkbox','is_pined','is_trashed' ,'color','reminder']
