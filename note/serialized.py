

from rest_framework import serializers
from .models import Notes, Label


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'note', 'label', 'url', 'archive', 'coll', 'image']


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'note']


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']


class LabelupdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['title', 'note', 'label', 'url', 'archive', 'coll',"copy",'checkbox','pin']
