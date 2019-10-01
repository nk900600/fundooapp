"""
thsi file is used for serilizing the existing models
"""
# from django.core import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    """
    registartion serializer is used for converting user data to json
    """
    class Meta:
        """
        Meta class to define model
        """
        model = Registration
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    user serializer is used for converting user details to to json
    """
    class Meta:
        """
        Meta class to define model
        """
        model = User
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
    """
    login serializer is used for converting username and password to json
    """
    class Meta:
        """
        Meta class to define model
        """
        model = User
        fields = ['username', 'password']


class ResetSerializer(serializers.ModelSerializer):
    """
    reset serializer is used for converting password to json
    """
    class Meta:
        """
        Meta class to define model
        """
        model = User
        fields = ['password']

class EmailSerializer(serializers.ModelSerializer):
    """
    email serializer is used for converting email to json
    """
    class Meta:
        """
        Meta class to define model
        """
        model = User
        fields = ['email']
