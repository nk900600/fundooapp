

from rest_framework import serializers
from .models import Notes, Lable


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'note','image']


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'note']


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['user', 'title', 'note', 'label', 'colaborator', 'archive', 'checkbox', 'pin', 'image',
                  'delete_note', 'copy']
