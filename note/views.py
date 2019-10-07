"""
 ******************************************************************************
 *  Purpose: will save user note
 *
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   30/09/2019
 ******************************************************************************
"""

import json
from urllib.parse import quote
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from fundoo import settings
from services.amazones3 import upload_file
from services.decorators import login_decorator
from .models import Notes, Lable
from note.serialized import NotesSerializer, UpdateSerializer, ShareSerializer



class Create(GenericAPIView):
    serializer_class = NotesSerializer


    @staticmethod
    @login_decorator
    def post(request):
        """
        :param request:  request from user
        :param args:
        :param kwargs:
        :return:  will save note details posted by user
        """
        smd = {'success': False, 'message': 'not a vaild note ', 'data': []}
        try:

            note = request.data['note']
            # images = request.data['image']
            user = request.user
            print(user)

            if note == "":
                return HttpResponse(json.dumps(smd))
            else:
                # upload_file(str(images), str(user) + str(images))
                # image_url = settings.url + str(user) + str(images)
                # users = User.objects.filter(email__in=colaborator)   #colabartor
                user = User.objects.get(pk=1)
                note_create = Notes(user_id=user.id, note=note)

                note_create.save()
                smd["success"] = True
                smd['message'] = 'note saved'

                return HttpResponse(json.dumps(smd))
        except (IntegrityError, Exception):
            return HttpResponse(json.dumps(smd))


class NoteShare(GenericAPIView):
    serializer_class = ShareSerializer

    def post(self, request):
        """
        :param request:  request from user
        :param args:
        :param kwargs:
        :return:  will save note details posted by user
        """
        smd = {'success': False, 'message': 'not a vaild note ', 'data': []}
        try:
            title = request.data['title']
            note = request.data['note']

            if note == "":
                return HttpResponse(json.dumps(smd))
            else:
                user = User.objects.get(pk=1)
                note_create = Notes(user_id=user.id, note=note, title=title)

                note_create.save()
                return redirect(
                    "https://twitter.com/intent/tweet?source=webclient&text=" + str(title) + "\n" + str(note))
        except (IntegrityError, Exception):
            return HttpResponse(json.dumps(smd))


class Update(GenericAPIView):
    serializer_class = UpdateSerializer

    def get(self, request, note_id):
        """
        :param request:  request from user
        :param args:
        :param kwargs:
        :return:  will render notes url
        """
        try:
            Notes.objects.get(id=note_id)
            return HttpResponse(json.dumps("hi"))
        except Exception:
            return HttpResponse(json.dumps('not a vaild url '))

    def put(self, request, note_id):
        smd = {'success': False, 'message': 'not a vaild note ', 'data': []}
        try:
            note = Notes.objects.get(id=note_id)
            user = request.data['user']
            title = request.data['title']
            note = request.data['note']
            label = request.data['label']
            collaborators = request.data['colaborator']
            archive = request.data['archive']
            checkbox = request.data['checkbox']
            pin = request.data['pin']
            images = request.data['image']
            delete = request.data["delete_note"]
            copy = request.data["copy"]

            validate_email(collaborators)

            if note == "":
                HttpResponse(json.dumps(smd))
            elif delete:
                Notes.objects.flter(id=note_id).delete()
                smd = {'success': True, 'message': 'note is deleted ', 'data': []}
                HttpResponse(json.dumps(smd))
            elif copy:
                new = Notes.objects.get(id=note_id)
                new.pk = None
                new.save()
                smd = {'success': True, 'message': 'note copy is created ', 'data': []}
                HttpResponse(json.dumps(smd))

            else:
                upload_file(str(images), str(user) + str(images))
                image_url = settings.url + str(user) + str(images)

                note_update = Notes.objects.filter(id=note_id).update(user_id=user, title=title, note=note,
                                                                      image=image_url,
                                                                      archive=archive, checkbox=checkbox, pin=pin)
                note_update.save()
                label = Lable.objects.filter(name=label)

                if label is None:
                    l = Lable.objects.create(name=label)
                    l.save()

                smd["success"] = True
                smd['message'] = 'note saved'
                return HttpResponse(json.dumps(smd))
        except (IntegrityError, TypeError, Exception):
            return HttpResponse(json.dumps(smd))

# class Archive(GenericAPIView):

#     def get(self, request, user_id):
#         pass

#     def post(self, request, user_id):
#         pass


# class Trash(GenericAPIView):

#     def get(self, request):
#         pass

#     def post(self, request, user_id):
#         pass


# class Reminders(GenericAPIView):

#     def get(self, request):
#         pass

#     def post(self, request):
#         pass


# class Lables(GenericAPIView):

#     def get(self, request, label):
#         pass

#     def post(self, request, label):
#         pass


# class Pin(GenericAPIView):

#     def get(self, request, user_id):
#         pass

#     def post(self, request, user_id):
#         pass
