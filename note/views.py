import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from note.serialized import NotesSerializer
from services.amazones3 import upload_file


class Create(GenericAPIView):

    serializer_class = NotesSerializer

    def get(self):
        return Response("hi")

    def post(self,request):
        title = request.data['title']
        note = request.data['note']
        label = request.data['label']
        colabrator = request.data['colabrator']
        archive = request.data['archive']
        checkbox = request.data['checkbox']
        pin = request.data['pin']
        image = request.FILE.get('image')

        file = request.FILES.get('file')
        print(file)
        # filename=str(username)+str(file)
        # upload_file(file,filename)
        # url="https://django-s3-files.s3.us-east-2.amazonaws.com/"+filename

        pass


