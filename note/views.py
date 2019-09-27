import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
from rest_framework.response import Response


class Create(APIView):

    def get(self):
        return Response("hi")

    def post(self,request):
        title = request.POST['title']
        note = request.POST['note']
        label = request.POST['label']
        colabrator = request.POST['colabrator']


        image = request.FILE.get('title')



        pass


