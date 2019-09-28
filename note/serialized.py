# from django.core import serializers

from rest_framework import serializers
from .models import Notes,Lable


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lable
        fields = '__all__'
