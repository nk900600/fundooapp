# from django.core import serializers
from rest_framework import serializers
from .models import Notes


class NotesSerializer(serializers.ModelSerializer):
    class meta:
        model = Notes
        fields = ["title", 'Note', 'image', 'archive', 'delete_note', 'label', 'colabrator', 'copy', 'checkbox', 'pin',
                  'trash']
