# from django.core import serializers

from rest_framework import serializers
from .models import Notes, Lable


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        # fields = '__all__'
        fields = ['title', 'note', 'label',  'archive', 'checkbox', 'pin',]


# class LabelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LableColabrator
#         fields = 'lable'


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['user', 'title', 'note', 'label', 'colaborator', 'archive', 'checkbox', 'pin', 'image',
                  'delete_note', 'copy']
