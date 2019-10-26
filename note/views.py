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
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone as tz
from django.shortcuts import get_object_or_404, render
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

from fundoo.settings import PORT, DB, file_handler, TWITTER_PAGE
from note.serialized import NotesSerializer, UpdateSerializer, ShareSerializer, LabelSerializer  # ArchiveSerializer
from lib.amazones3 import AmazoneS3
from note.decorators import login_decorator, label_coll_validator_put, label_coll_validator_post
from lib.redis import red
# import logging
from .models import Notes, Label
from pymitter import EventEmitter

ee = EventEmitter()

s3 = AmazoneS3()
# import django.core.files.uploadedfile as d

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


# @method_decorator(login_decorator, name='dispatch')
class Create(GenericAPIView):
    serializer_class = NotesSerializer
    #
    # def get(self,request):
    #     # try:
    #     user=request.user
    #     notes=Notes.objects.filter(user_id=user.id)
    #     paginator = Paginator(notes.values(), 25)
        # print(paginator)
        # page = request.GET.get('http://localhost:8000/api/note/')
        # contacts = paginator.get_page(paginator)
        #
        # return render(request, "user/pagination.html",{"data": contacts})
        # return render(request, "user/pagination.html", {"data": notes.values()})
        # except Exception:
        #     return HttpResponse("dgde")

    def get(self,request):
        notes_list = Notes.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(notes_list, 20)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return render(request, 'user/test.html', {'users': users})


    # parser_classes = (FormParser,FileUploadParser)
    @staticmethod
    @label_coll_validator_post
    def post(request):
        """
        :param request:  request from user
        :return:  will save note details posted by user
        """
        try:
            # data is taken from user

            data = request.data
            user = request.user
            data['user'] = user.id
            collaborator_list = []  # empty coll  list is formed where data is input is converted to id
            label_list = []  # empty label list is formed where data is input is converted to id
            try:
                label = data["label"]
                # for loop is used for the getting label input and coll input ids
                for name in label:
                    label_name = Label.objects.filter(user_id=user.id, name=name)
                    label_id = label_name.values()[0]['id']
                    label_list.append(label_id)
                data['label'] = label_list
            except KeyError:
                pass
            try:
                collaborator = data['collaborator']
                # for loop is used for the getting label input and coll input ids
                for email in collaborator:
                    email_id = User.objects.filter(email=email)
                    id = email_id.values()[0]['id']
                    collaborator_list.append(id)
                data['collaborator'] = collaborator_list
            except KeyError:
                pass

            serializer = NotesSerializer(data=data, partial=True)

            if serializer.is_valid():
                note_create = serializer.save(user=user)
                red.set(note_create.id, str(json.dumps(serializer.data)))  # created note is cached in redis
                response = {'success': True, 'message': "note created", 'data': []}
                # logging.info("new note is created")
                logger.info("note is created")
                return HttpResponse(json.dumps(response, indent=2), status=201)
            response = {'success': False, 'message': "note was not created", 'data': []}
            print(serializer.error_messages)
            # return HttpResponse(serializer.error_messages())
            logger.error("note was not created")
            return HttpResponse(json.dumps(response, indent=2), status=400)
        except Exception as e:
            response = {'success': False, 'message': "something went wrong", 'data': []}
            return Response(response, status=404)


@method_decorator(login_decorator, name='dispatch')
class Update(GenericAPIView):
    serializer_class = UpdateSerializer

    def get(self, request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        try:
            # pdb.set_trace()
            # get_object_or_404(Notes, id=note_id)
            redis_data = red.get(str(note_id))
            if redis_data is None:
                note = Notes.objects.filter(id=note_id)
                serialized_data = NotesSerializer(note, many=True)
                logger.info("note was fetched from database")
                return HttpResponse(json.dumps(serialized_data.data, indent=1))
            logger.info("note was fetched form redis")
            return HttpResponse(redis_data)
        except Notes.DoesNotExist:
            response = {'success': False, 'message': "note does not exists", 'data': []}
            return Response(response, status=404)
        except Exception:
            response = {'success': False, 'message': "something went wrong", 'data': []}
            return Response(response, status=404)

    @staticmethod
    @label_coll_validator_put
    def put(request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        try:
            # data is fetched from user
            instance = Notes.objects.get(id=note_id)
            data = request.data
            collaborator_list = []  # empty coll  list is formed where data is input is converted to id
            label_list = []  # empty label list is formed where data is input is converted to id
            try:
                label = data["label"]
                # for loop is used for the getting label input and coll input ids
                for name in label:
                    label_values = Label.objects.filter(user_id=1, name=name)
                    label_id = label_values.values()[0]['id']
                    label_list.append(label_id)
                data['label'] = label_list
            except KeyError:
                logger.error("key error on label as label field was not given")
                pass
            try:
                collaborator = data['collaborator']
                # for loop is used for the getting label input and coll input ids
                for email in collaborator:
                    emails = User.objects.filter(email=email)
                    email_id = emails.values()[0]['id']
                    collaborator_list.append(email_id)
                data['collaborator'] = collaborator_list
            except KeyError:
                pass
            serializer = NotesSerializer(instance, data=data, partial=True)
            # here serialized data checked for validation and saved
            if serializer.is_valid():
                note_create = serializer.save()
                red.set(note_create.id, str(json.dumps(serializer.data)))  # created note is cached in redis
                logger.info("note was updated")
                response = {'success': True, 'message': "note created", 'data': []}
                return HttpResponse(json.dumps(response, indent=2), status=200)
            logger.error("note was not updated")
            response = {'success': False, 'message': "note was not created", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=400)
        except Exception as e:
            response = {'success': False, 'message': "something went wrong", 'data': []}
            return Response(response, status=404)

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
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            user = request.user
            labels = Label.objects.filter(user_id=user.id)
            label_name = []
            for i in labels:
                label_name.append(i.name)
            return Response(label_name, status=200)
        except Exception:
            return Response(response, status=400)

    def post(self, request):
        """
        :param request: request from user
        :return: will get all lables created by user
        """
        response = {"success": False, "message": "something went wrong", "data": []}
        try:
            label = request.data["name"]
            user = request.user
            if Label.objects.filter(user_id=user.id, name=label).exists():
                logger.warning("note is already exists")
                response = {"success": False, "message": "note is already exists", "data": label}
                return Response(response, status=400)

            Label.objects.create(user_id=user.id, name=label)
            logger.info("note is created")
            response = {"success": True, "message": "note is created", "data": label}
            return Response(response, status=201)
        except Exception:
            return Response(response, status=404)


@method_decorator(login_decorator, name='dispatch')
class LabelsUpdate(GenericAPIView):
    serializer_class = LabelSerializer

    def put(self, request, label_id):
        """
        :param request: request from user
        :param name: name of the label
        :return: will update the data
        """
        response = {
            "success": False,
            "message": "Something bad happened",
            "data": []
        }
        try:
            user = request.user
            requestBody = json.loads(request.body)
            label_name = requestBody['name']
            label = get_object_or_404(Label, id=label_id, user_id=user.id)
            label.name = label_name
            label.save()
            response["message"] = "label updated successfully"
            response["data"] = [label_name]
            response["success"] = True
            return HttpResponse(json.dumps(response, indent=2), status=200)
        except KeyError:
            logger.warning("label does not exist")
            response["message"] = "label does not exist"
            return Response(response, status=400)
        except Exception as e:
            return Response(response, status=404)

    def delete(self, request, name):
        """
        :param request: request from user
        :param name: name of the label
        :return: will delete the data
        """
        response = {
            "success": False,
            "message": "Something bad happened",
            "data": {}
        }
        try:
            user = request.user
            label_name = Label.objects.get(name=name, user_id=user.id)
            label_name.delete()
            logger.info("note is deleted")
            response = {"success": True, "message": "note is deleted", "data": []}
            return Response(response, status=204)
        except Exception as e:
            return Response(response, status=404)


# @method_decorator(login_decorator, name='dispatch')
class Archive(GenericAPIView):
    # serializer_class = ArchiveSerializer

    def get(self, request):
        user = request.user
        no = Notes.objects.filter(user_id=user.id, is_archive=True)
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
        # pdb.set_trace()
        user = request.user
        try:
            reminder_list = Notes.objects.all().values_list('reminder', flat=True)
            fired = []
            pending = []
            for i in range(len(reminder_list.values())):
                if reminder_list.values()[i]['reminder'] is None:
                    continue
                elif tz.now() > reminder_list.values()[i]['reminder']:
                    fired.append(reminder_list.values()[i])
                else:
                    pending.append(reminder_list.values()[i])
            reminder = {
                'fired': fired,
                'pending': pending
            }
            logger.info("Reminders data is loaded")
            return HttpResponse(reminder.values(), status=200)
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
                return redirect(TWITTER_PAGE + str(title) + "\n" + str(note))
        except (IntegrityError, Exception):
            return HttpResponse(json.dumps(smd, indent=2), status=400)
