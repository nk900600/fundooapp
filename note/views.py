"""
 ******************************************************************************
 *  Purpose: will save user note
 *
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   30/09/2019
 ******************************************************************************
"""

from django.contrib.auth.models import AbstractBaseUser
import json
from urllib.parse import quote
from django.views.generic import View
from django.core.files.storage import default_storage
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User


from fundoo import settings
from services import redis
from services.amazones3 import upload_file
from services.decorators import login_decorator
from .models import Notes, Label
from storages.backends.s3boto3 import  S3Boto3Storage
from note.serialized import NotesSerializer, UpdateSerializer, ShareSerializer, LabelSerializer

# def url(self, name, parameters=None, expire=None):

def labelvalidator(label,user_id):
    lab = []
    try:
        z = 0
        for i in range(len(label)):
            z = i
            ll=Label.objects.filter(user_id=user_id)
            lab.append(ll.values()[i]["name"])
            print("????????????????????????????????????")
    except Exception:
        fun = [True,lab]
        return fun

# z= storages.backends.s3boto3.S3Boto3Storage
def collvalidator(collaborators):
    for i in collaborators:
        try:
            User.objects.get(email=i)
        except Exception:
            return True


# @method_decorator(login_decorator,name='dispatch')
class Create(GenericAPIView):
    serializer_class = NotesSerializer

    # @staticmethod
    # @login_decorator
    # def get(request):
    #     notes = Notes.objects.filter(id=210)
    #     note_ser = NotesSerializer(notes, many=True)
    #     return Response(note_ser.data)
    # data = Notes.objects.filter(id=53)
    # return HttpResponse(json.dumps(data))

    # @staticmethod
    # @login_decorator
    def post(self,request):
        """
        :param request:  request from user
        :param args:
        :param kwargs:
        :return:  will save note details posted by user
        """
        smd = {'success': False, 'message': 'not a vaild note ', 'data': []}
        user_id = request.data['user']
        title = request.data['title']
        note = request.data['note']
        label = request.data['label']
        url = request.data['url']
        archive = request.data['archive']
        collaborators = request.data['coll']
        image = request.data["image"]
        # print(user)

        print("ddd")
        z=labelvalidator(label,user_id)
        print(z[1])
        if labelvalidator(label,user_id)[0]:
            smd['message'] = " label is not added in note as it is not a vaild label  "
            return HttpResponse(json.dumps(smd))
        #
        elif collvalidator(collaborators):
            smd['message'] = "  email is not registered  "
            return HttpResponse(json.dumps(smd))

        # z = NotesSerializer(data=request.data)


        # if z.is_valid():
        #    z.save()
        #
        if note == "":
            return HttpResponse(json.dumps(smd))
        else:


            # users = User.objects.filter(email__in=Collaborators)   #collaborators
            #

            upload_file(str(image), "image/" + str(22) + str(image))

            note_create = Notes(user_id=1, title=title, note=note, url=url,
                                image=image)

            note_create.save()
            ll = Notes.objects.filter(id=note_create.id)
            p = NotesSerializer(ll, many=True)
            print(p.data[0]["image"])

            for i in labelvalidator(label,user_id)[1]:
                z = Label.objects.get(name=i).id
                note_create.label.add(z)
            for i in collaborators:
                z = User.objects.get(email=i).id
                note_create.coll.add(z)

            smd["success"] = True
            smd['message'] = 'note saved'
            # smd["data"] = ser.data['image']

            return HttpResponse(json.dumps(smd))
        #  return render(request,"user/index.html", {"data": smd['data']})
        # except (IntegrityError, Exception):
        #     return HttpResponse(json.dumps(smd))


class Update(GenericAPIView):
    serializer_class = UpdateSerializer
    @staticmethod
    def get(request, note_id):
        """
        :param request:  request from user
        :param args:
        :param kwargs:
        :return:  will render notes url
        """
        try:
            ll = Notes.objects.filter(id=9)
            p = NotesSerializer(ll, many=True)
            print(p.data[0]["image"])
            return HttpResponse(json.dumps(p.data[0]["image"]))
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
            collaborators = request.data['coll']
            archive = request.data['archive']
            checkbox = request.data['checkbox']
            pin = request.data['pin']
            images = request.data['image']
            delete = request.data["delete_note"]
            copy = request.data["copy"]

            # validate_email(collaborators)

            if labelvalidator(label):
                smd['message'] = " label is not added in note as it is not a vaild label  "
                return HttpResponse(json.dumps(smd))

            elif collvalidator(collaborators):
                smd['message'] = "  email is not registered  "
                return HttpResponse(json.dumps(smd))

            elif copy:
                new = Notes.objects.get(id=note_id)
                new.pk = None
                new.save()
                smd = {'success': True, 'message': 'note copy is created ', 'data': []}
                HttpResponse(json.dumps(smd))

            else:
                # upload_file(str(images), str(user) + str(images))
                # image_url = settings.url + str(user) + str(images)

                note_update = Notes.objects.filter(id=note_id).update(title=title, note=note,
                                                                      archive=archive, checkbox=checkbox, pin=pin)
                note_update.save()
                for i in label:
                    z = Label.objects.get(name=i).id
                    note_update.label.add(z)
                for i in collaborators:
                    z = User.objects.get(email=i).id
                    note_update.coll.add(z)

                smd["success"] = True
                smd['message'] = 'note saved'
                return HttpResponse(json.dumps(smd))
        except (IntegrityError, TypeError, Exception):
            return HttpResponse(json.dumps(smd))

    def delete(self, request, note_id):
        smd = {'success': False, 'message': 'not a vaild note ', 'data': []}
        try:
            z= Notes.objects.filter(id=note_id)
            z.delete()
            smd = {'success': True, 'message': 'note is deleted ', 'data': []}
            return HttpResponse(json.dumps(smd))
        except Exception:
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


class LabelsCreate(GenericAPIView):
    serializer_class = LabelSerializer

    # def get(self,request):
    #     smd = {"success": False, "message": "not a vaild note id", "data": []}
    #
    #     z = Label.objects.filter(user_id=1)
    #     lab = []
    #     for i in z:
    #         lab.append(i.name)
    #     # y = Label.objects.filter(user_id=user_id)
    #     # yy = LabelSerializer(y, many=True)
    #     return HttpResponse(json.dumps(lab))

    def post(self, request):
        smd = {"success": False, "message": "label with same name already exist", "data": []}
        label = request.data["name"]

        try:

            newlabel = Label.objects.create(user_id=1, name=label)

            newlabel.save()
            smd["success"] = True
            smd["message"] = "note is created"
            smd["data"] = label
            return HttpResponse(json.dumps(smd))
        except IntegrityError:

            return HttpResponse(json.dumps(smd))


class LabelsUpdate(GenericAPIView):
    serializer_class = LabelSerializer

    def put(self, request, name):
        smd = {"success": False, "message": "please check label name you entered or label with same name already exist",
               "data": []}
        try:
            label = request.data["name"]
            lab = Label.objects.get(name=name)
            lab.name = label
            lab.save()
            smd["success"] = True
            smd["message"] = "note is update"
            smd["data"] = label
            return HttpResponse(json.dumps(smd))
        except (IntegrityError, Exception):
            return HttpResponse(json.dumps(smd))

    def delete(self, request, name):
        smd = {"success": False, "message": "not a vaild note name", "data": []}
        try:
            lab = Label.objects.get(name=name)
            lab.delete()
            smd["success"] = True
            smd["message"] = "note is deleted"
            return HttpResponse(json.dumps(smd))
        except (Exception, TypeError):
            return HttpResponse(json.dumps(smd))


# class Pin(GenericAPIView):

#     def get(self, request, user_id):
#         pass

#     def post(self, request, user_id):
#         pass


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
