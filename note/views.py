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
from services.redis import Redis
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from services.amazones3 import upload_file
from services.decorators import login_decorator
from .models import Notes, Label
from note.serialized import NotesSerializer, UpdateSerializer, ShareSerializer, LabelSerializer, LabelupdateSerializer

redis = Redis()

@method_decorator(login_decorator, name='dispatch')
class Create(GenericAPIView):
    serializer_class = NotesSerializer

    # def get(self, request):
    #     """
    #     :param request: request user data
    #     :return: will print all the user data
    #     """
    #     user =request.user
    #     note = Notes.objects.filter(user_id= user.id)
    #     serialized_data = NotesSerializer(note, many=True)
    #     return HttpResponse(json.dumps(serialized_data.data, indent=1))

    def post(self, request):
        """
        :param request:  request from user
        :param args:
        :param kwargs:
        :return:  will save note details posted by user
        """

        user = request.user
        try:

            title = request.data['title']
            note = request.data['note']
            label = request.data['label']
            url = request.data['url']
            archive = request.data['archive']
            collaborators = request.data['coll']
            try:
                image = request.data["image"]
            except (FileNotFoundError, Exception):
                smd = {'success': False, 'message': 'not a valid image or path ', 'data': []}
                return HttpResponse(json.dumps(smd))

            if labelvalidator(label, user.id)[0]:
                smd = {'success': False, 'message': 'label is not created by this user or user does not exist',
                       'data': []}
                return HttpResponse(json.dumps(smd))

            if collvalidator(collaborators):
                smd = {'success': False, 'message': 'email not vaild',
                       'data': []}
                return HttpResponse(json.dumps(smd))

            if note == "":
                smd = {'success': False, 'message': 'note is empty ', 'data': []}
                return HttpResponse(json.dumps(smd))
            else:
                upload_file(str(image), "image/" + str(image))
                note_create = Notes(user_id=user.id, title=title, note=note, url=url, checkbox=False,
                                    copy=False, pin=False, delete_note=False, image=image, archive=archive)
                note_create.save()
                print(note_create.id)
                for name in label:
                    lab_id = Label.objects.get(name=name).id
                    note_create.label.add(lab_id)
                try:
                    for email in collaborators:
                        email_id = User.objects.filter(email=email)
                        id = email_id.values()[0]['id']
                        note_create.coll.add(id)
                    note_data = Notes.objects.filter(id=note_create.id)

                    redis.set(note_create.id, str(note_data.values()).encode('utf-8'))
                    smd = {'success': True, 'message': 'note saved', 'data': []}
                except IndexError:
                    smd = {'success': False, 'message': 'not a vaild email address ', 'data': []}

        except (IntegrityError, Exception):
            smd = {'success': False, 'message': "some thing went wrong", 'data': []}
        return HttpResponse(json.dumps(smd))


@method_decorator(login_decorator, name='dispatch')
class Update(GenericAPIView):
    serializer_class = UpdateSerializer

    def get(self, request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        Notes.objects.get(id=note_id)
        note = Notes.objects.filter(id=note_id)
        serialized_data = NotesSerializer(note, many=True)
        return HttpResponse(json.dumps(serialized_data.data, indent=1))

    def put(self, request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        smd = {'success': False, 'message': 'not a vaild note ', 'data': []}
        user = request.user

        try:
            Notes.objects.get(id=note_id)
            title = request.data['title']
            note = request.data['note']
            label = request.data['label']
            collaborators = request.data['coll']
            archive = request.data['archive']
            checkbox = request.data['checkbox']
            pin = request.data['pin']
            copy = request.data["copy"]

            if labelvalidator(label, user.id)[0]:
                smd = {'success': False, 'message': 'label is not created by this user or user doesnot exist',
                       'data': []}
                return HttpResponse(json.dumps(smd))

            if collvalidator(collaborators):
                smd = {'success': False, 'message': 'email not vaild', 'data': []}
                return HttpResponse(json.dumps(smd))

            if note == "":
                smd = {'success': False, 'message': 'note is empty ', 'data': []}
                # return HttpResponse(json.dumps(smd))

            elif copy:
                new = Notes.objects.get(id=note_id)
                new.pk = None
                new.save()

            else:

                Notes.objects.filter(id=note_id).update(title=title, note=note, archive=archive, checkbox=checkbox,
                                                        pin=pin)

                update = Notes.objects.get(id=note_id)
                for i in label:
                    z = Label.objects.get(name=i).id
                    update.label.add(z)
                for i in collaborators:
                    z = User.objects.get(email=i).id
                    update.coll.add(z)

                smd["success"] = True
                smd['message'] = 'note saved'
                return HttpResponse(json.dumps(smd))
        except (IntegrityError, TypeError, Exception):
            HttpResponse(json.dumps(smd))
        return HttpResponse(json.dumps(smd))

    def delete(self, request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        smd = {'success': False, 'message': 'not a vaild note ', 'data': []}
        try:
            note = Notes.objects.get(id=note_id)
            note.delete()
            smd = {'success': True, 'message': 'note is deleted ', 'data': []}
            return HttpResponse(json.dumps(smd))
        except KeyError:
            return HttpResponse(json.dumps(smd))


@method_decorator(login_decorator, name='dispatch')
class LabelsCreate(GenericAPIView):
    serializer_class = LabelSerializer

    def get(self, request):
        """
        :param request: request from user
        :return: will get all lables created by user
        """
        user = request.user
        labels = Label.objects.filter(user_id=user.id)
        lab = []
        for i in labels:
            lab.append(i.name)
        return HttpResponse(json.dumps(lab))

    def post(self, request):
        """
        :param request: request from user
        :return: will get all lables created by user
        """
        smd = {"success": False, "message": "label with same name already exist", "data": []}
        user = request.user
        label = request.data["name"]

        # try:

        newlabel = Label.objects.create(user_id=user.id, name=label)
        newlabel.save()
        smd = {"success": True, "message": "note is created", "data": label}
        return HttpResponse(json.dumps(smd))
        # except IntegrityError:
        #     return HttpResponse(json.dumps(smd))


@method_decorator(login_decorator, name='dispatch')
class LabelsUpdate(GenericAPIView):
    serializer_class = LabelupdateSerializer

    def put(self, request, name):
        """
        :param request: request from user
        :param name: name of the label
        :return: will update the data
        """
        user = request.user
        label = request.data["name"]
        lab = Label.objects.get(name=name, user_id=user.id)
        lab.name = label
        lab.save()
        smd = {"success": True, "message": "note is update", "data": [label]}
        return HttpResponse(json.dumps(smd))

    def delete(self, request, name):
        """
        :param request: request from user
        :param name: name of the label
        :return: will delete the data
        """
        user = request.user
        lab = Label.objects.get(name=name, user_id=user.id)
        lab.delete()
        smd = {"success": True, "message": "note is deleted", "data": []}
        return HttpResponse(json.dumps(smd))


# class Pin(GenericAPIView):

#     def get(self, request, user_id):
#         pass

#     def post(self, request, user_id):
#         pass

@method_decorator(login_decorator, name='dispatch')
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



def labelvalidator(label, user_id):
    lab = []
    try:
        z = 0
        # print(len(label))
        ll = Label.objects.filter(user_id=user_id)
        for i in range(len(label)):
            Label.objects.get(name=label[i], user_id=user_id)
            lab.append(ll.values()[i]["name"])
        return False, lab
    except Exception:
        return True, lab

def collvalidator(collaborators):
    try:
        for email in collaborators:
            email_id = User.objects.filter(email=email)
            id = email_id.values()[0]['id']
    except Exception:
        return True