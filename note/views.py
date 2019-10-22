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
import logging
from datetime import datetime, timedelta
from functools import wraps
import django
from django.core import serializers
from django.utils import timezone as tz
from django.shortcuts import get_object_or_404
import redis
import pdb
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.response import Response

from fundoo.settings import PORT, DB, file_handler
from note.serialized import NotesSerializer, UpdateSerializer, ShareSerializer, LabelSerializer, LabelupdateSerializer, \
    ArchiveSerializer
from lib.amazones3 import AmazoneS3
from note.decorators import login_decorator, label_coll_validator_put, label_coll_validator_post
from lib.redis import red
# import logging
from .models import Notes, Label
from pymitter import EventEmitter
ee = EventEmitter()

s3 = AmazoneS3()
#import django.core.files.uploadedfile as d

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

@method_decorator(login_decorator, name='dispatch')
class Create(GenericAPIView):
    serializer_class = NotesSerializer

    # parser_classes = (FormParser,FileUploadParser)
    @staticmethod
    @label_coll_validator_post
    def post(request):
        """
        :param request:  request from user
        :return:  will save note details posted by user
        """
        # data is taken from user
        data = request.data
        user = request.user
        data['user'] = user.id
        coll_list = []  # empty coll  list is formed where data is input is converted to id
        label_list = []  # empty label list is formed where data is input is converted to id
        try:
            label = data["label"]
            # for loop is used for the getting label input and coll input ids
            for name in label:
                lab_id = Label.objects.filter(user_id=1, name=name)
                id = lab_id.values()[0]['id']
                label_list.append(id)
            data['label'] = label_list
        except KeyError:
            pass
        try:
            coll = data['coll']
            # for loop is used for the getting label input and coll input ids
            for email in coll:
                email_id = User.objects.filter(email=email)
                id = email_id.values()[0]['id']
                coll_list.append(id)
            data['coll'] = coll_list
        except KeyError:
            pass

        serializer = NotesSerializer(data=data, partial=True)

        if serializer.is_valid():
            note_create = serializer.save(user=user)
            red.set(note_create.id, str(json.dumps(serializer.data)))  # created note is cached in redis
            smd = {'success': True, 'message': "note created", 'data': []}
            # logging.info("new note is created")
            logger.info("note is created")
            return HttpResponse(json.dumps(smd, indent=2), status=201)
        smd = {'success': False, 'message': "note was not created", 'data': []}
        print(serializer.error_messages)
        # return HttpResponse(serializer.error_messages())
        logger.error("note was not created")
        return HttpResponse(json.dumps(smd, indent=2), status=400)


@method_decorator(login_decorator, name='dispatch')
class Update(GenericAPIView):
    serializer_class = UpdateSerializer

    def get(self, request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        # pdb.set_trace()
        get_object_or_404(Notes, id=note_id)
        redis_data = red.get(str(note_id))
        if redis_data is None:
            note = Notes.objects.filter(id=note_id)
            serialized_data = NotesSerializer(note, many=True)
            logger.info("note was fetched from database")
            return HttpResponse(json.dumps(serialized_data.data, indent=1))
        logger.info("note was fetched form redis")
        return HttpResponse(redis_data)

    @staticmethod
    @label_coll_validator_put
    def put(request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """

        instance = Notes.objects.get(id=note_id)
        # data is fetched from user
        data = request.data
        coll_list = []  # empty coll  list is formed where data is input is converted to id
        label_list = []  # empty label list is formed where data is input is converted to id
        try:
            label = data["label"]
            # for loop is used for the getting label input and coll input ids
            for name in label:
                lab_id = Label.objects.filter(user_id=1, name=name)
                id = lab_id.values()[0]['id']
                label_list.append(id)
            data['label'] = label_list
        except KeyError:
            logger.error("keyerror on label as label field was not given")
            pass
        try:
            coll = data['coll']
            # for loop is used for the getting label input and coll input ids
            for email in coll:
                email_id = User.objects.filter(email=email)
                id = email_id.values()[0]['id']
                coll_list.append(id)
            data['coll'] = coll_list
        except KeyError:
            pass
        serializer = NotesSerializer(instance, data=data, partial=True)
        # here serialized data checked for validation and saved
        if serializer.is_valid():
            note_create = serializer.save()
            red.set(note_create.id, str(json.dumps(serializer.data)))  # created note is cached in redis
            logger.info("note was updated")
            smd = {'success': True, 'message': "note created", 'data': []}
            return HttpResponse(json.dumps(smd, indent=2), status=200)
        logger.error("note was not updated")
        smd = {'success': False, 'message': "note was not created", 'data': []}
        return HttpResponse(json.dumps(smd, indent=2), status=400)

    def delete(self, request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        smd = {'success': False, 'message': 'not a vaild note ', 'data': []}
        try:
            note = get_object_or_404(Notes, id=note_id)
            note.delete_note = True
            note.save()
            logger.info("note was deleted")
            smd = {'success': True, 'message': 'note is deleted ', 'data': []}
            return HttpResponse(json.dumps(smd, indent=2), status=201)
        except KeyError:
            logger.error("note was not deleted")
            return HttpResponse(json.dumps(smd, indent=2), status=400)


@method_decorator(login_decorator, name='dispatch')
class LabelsCreate(GenericAPIView):
    serializer_class = LabelSerializer

    def get(self, request):
        """
        :param request: request from user
        :return: will get all lables created by user
        """
        user = request.user
        print(user)
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
        user = request.user
        label = request.data["name"]
        if Label.objects.filter(user_id=user.id, name=label).exists():
            logger.warning("note is already exists")
            smd = {"success": False, "message": "note is already exists", "data": label}
            return HttpResponse(json.dumps(smd, indent=2), status=400)

        Label.objects.create(user_id=user.id, name=label)
        logger.info("note is created")
        smd = {"success": True, "message": "note is created", "data": label}
        return HttpResponse(json.dumps(smd, indent=2), status=201)


@method_decorator(login_decorator, name='dispatch')
class LabelsUpdate(GenericAPIView):
    serializer_class = LabelupdateSerializer

    def put(self, request, name):
        """
        :param request: request from user
        :param name: name of the label
        :return: will update the data
        """
        try:
            # pdb.set_trace()
            user = request.user
            # label = request.data["name"]
            # print(type(request.body))
            res=json.loads(request.body)
            label=res['name']
            lab = get_object_or_404(Label, name=name, user_id=user.id)
            lab.name = label
            lab.save()
            logger.info("label is update")
            smd = {"success": True, "message": "label is update", "data": [label]}
            return Response(smd, status=200)
        except KeyError:
            logger.warning("label does not exist")
            smd = {"success": True, "message": "label does not exist", "data": []}
            return Response(smd, status=400)


    def delete(self, request, name):
        """
        :param request: request from user
        :param name: name of the label
        :return: will delete the data
        """
        user = request.user
        lab = Label.objects.get(name=name, user_id=user.id)
        lab.delete()
        logger.info("note is deleted")
        smd = {"success": True, "message": "note is deleted", "data": []}
        return HttpResponse(json.dumps(smd, indent=2),status=204)


@method_decorator(login_decorator, name='dispatch')
class Archive(GenericAPIView):
    # serializer_class = ArchiveSerializer

    def get(self, request):
        user = request.user
        no = Notes.objects.filter(user_id=user.id, archive=True)
        logger.info("archive data is loaded")
        return HttpResponse(no.values(), status=200)


# @method_decorator(login_decorator, name='dispatch')
class Trash(GenericAPIView):
    # serializer_class = ArchiveSerializer

    def get(self, request):
        user = request.user
        no = Notes.objects.filter(user_id=user.id, delete_note=True)
        logger.info("Trash data is loaded")
        return HttpResponse(no.values())


@method_decorator(login_decorator, name='dispatch')
class Reminders(GenericAPIView):

    def get(self, request):
        end_dt = tz.now() + tz.timedelta(days=10)  # you should tune the value
        start_dt = tz.now()  #
        user = request.user
        try:
            no = Notes.objects.filter(user_id=user.id, reminder__range=(start_dt, end_dt))
            logger.info("Reminders data is loaded")
            return HttpResponse(no.values(), status=200)
        except TypeError:
            logger.info("no reminder set")
            smd = {"success": False, "message": "no reminder set", 'data': []}
            return HttpResponse(json.dumps(smd), status=200)


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
            user = request.user

            if note == "":
                return HttpResponse(json.dumps(smd))
            else:
                user = get_object_or_404(User, pk=user.id)
                note_create = Notes(user_id=user.id, note=note, title=title)

                note_create.save()
                return redirect(
                    "https://twitter.com/intent/tweet?source=webclient&text=" + str(title) + "\n" + str(note))
        except (IntegrityError, Exception):
            return HttpResponse(json.dumps(smd, indent=2), status=400)
