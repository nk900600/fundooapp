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
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fundoo.settings import PORT, DB, file_handler, TWITTER_PAGE
from note.serialized import NotesSerializer, UpdateSerializer, ShareSerializer, LabelSerializer  # ArchiveSerializer
from lib.amazones3 import AmazoneS3
from note.decorators import login_decorator, label_coll_validator_put, LabelCollaborators  # , label_coll_validator_post
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


@method_decorator(login_decorator, name='dispatch')
class Create(GenericAPIView):
    serializer_class = NotesSerializer
    @LabelCollaborators
    def get(self, request):
        notes_list = Notes.objects.all()
        page = request.GET.get('page')
        paginator = Paginator(notes_list, 1)
        user = request.user

        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            logger.warning("got %s error for getting note for user %s", str(PageNotAnInteger), user.username)
            notes = paginator.page(1)
        except EmptyPage:
            logger.warning("got %s error for getting note for user %s", EmptyPage, user)
            notes = paginator.page(paginator.num_pages)
        logger.info("all the notes are rendered to html page for user %s", user)
        return render(request, 'user/pagination.html', {'notes': notes})

    # parser_classes = (FormParser,FileUploadParser)
    @staticmethod
    # @label_coll_validator_post
    def post(request):
        """
        :param request:  request from user
        :return:  will save note details posted by user
        """
        user = request.user
        try:
            # data is taken from user
            # pdb.set_trace()
            data = request.data
            user = request.user
            # data['user'] = user.id
            collaborator_list = []  # empty coll  list is formed where data is input is converted to id
            try:
                # for loop is used for the getting label input and coll input ids
                data["label"] = [Label.objects.filter(user_id=user.id, name=name).values()[0]['id'] for name in
                                 data["label"]]
            except KeyError:
                logger.debug('label was not added by the user %s', user)
                pass
            try:
                collaborator = data['collaborators']
                # for loop is used for the getting label input and coll input ids
                for email in collaborator:
                    email_id = User.objects.filter(email=email)
                    user_id = email_id.values()[0]['id']
                    collaborator_list.append(user_id)
                data['collaborators'] = collaborator_list
                print(data['collaborators'])
            except KeyError:
                logger.debug('collaborator was not added by the user %s', user)
                pass

            serializer = NotesSerializer(data=data, partial=True)
            # print(serializer.initial_data)

            if serializer.is_valid():
                note_create = serializer.save(user=user)
                red.hmset(user.id + "note",
                          {note_create.id: str(json.dumps(serializer.data))})  # created note is cached in redis
                response = {'success': True, 'message': "note created", 'data': []}
                # logging.info("new note is created")
                logger.info("note is created for %s with note id as %s", user, note_create.id)
                return HttpResponse(json.dumps(response, indent=2), status=201)
            logger.error(" %s for  %s", user, serializer.errors)
            response = {'success': False, 'message': "note was not created", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=400)
        except Exception as e:
            logger.error("got %s error for creating note for user %s", str(e), user)
            response = {'success': False, 'message': "something went wrong", 'data': []}
            return Response(response, status=400)


@method_decorator(login_decorator, name='dispatch')
class Update(GenericAPIView):
    serializer_class = UpdateSerializer

    # permission_classes = (IsAuthenticated,)

    def get(self, request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        try:
            # pdb.set_trace()

            redis_data = red.hmget(request.user.id + "note", str(note_id))
            user = request.user
            print(user)
            if redis_data is None:
                note = Notes.objects.filter(id=note_id)
                serialized_data = NotesSerializer(note, many=True)
                logger.info("note was fetched from database for user %s", user)
                return HttpResponse(json.dumps(serialized_data.data, indent=1))
                # return HttpResponse(json.dumps(serialized_data.data, indent=1))
            logger.info("note was fetched form redis for user %s", user)
            return HttpResponse(redis_data)
        except Notes.DoesNotExist:
            logger.error("Note id doesnt exists, node_id:", note_id)
            response = {'success': False, 'message': "note does not exists", 'data': []}
            return Response(response, status=404)
        except Exception as e:
            logger.error("Unknown error while updating the note, %s %s:", note_id, str(e))
            response = {'success': False, 'message': str(e), 'data': []}
            return Response(response, status=404)

    @staticmethod
    @label_coll_validator_put
    def put(request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        user = request.user
        try:
            # data is fetched from user
            instance = Notes.objects.get(id=note_id)
            data = request.data
            collaborator_list = []  # empty coll  list is formed where data is input is converted to id
            try:
                label = data["label"]
                data['label'] = [Label.objects.get(name=name, user_id=request.user.id).id for name in label]
            except KeyError:
                logger.debug('label was not added by the user %s', user)
                pass
            try:
                collaborator = data['collaborators']
                # for loop is used for the getting label input and coll input ids
                for email in collaborator:
                    emails = User.objects.filter(email=email)
                    user_id = emails.values()[0]['id']
                    collaborator_list.append(user_id)
                data['collaborators'] = collaborator_list
            except KeyError:
                logger.debug('collaborators was not added by the user %s', user)
                pass
            serializer = NotesSerializer(instance, data=data, partial=True)
            # here serialized data checked for validation and saved
            if serializer.is_valid():
                note_create = serializer.save()
                red.hmset(user.id + "note",
                          {note_create.id: str(json.dumps(serializer.data))})
                logger.info("note was updated with note id :%s for user :%s ", note_id, user)
                response = {'success': True, 'message': "note updated", 'data': []}
                return HttpResponse(json.dumps(response, indent=2), status=200)
            logger.error("note was updated with note id :%s for user :%s ", note_id, user)
            response = {'success': False, 'message': "note was not created", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=400)
        except Exception as e:
            logger.error("got error :%s for user :%s while updating note id :%s", str(e), user, note_id)
            response = {'success': False, 'message': str(e), 'data': []}
            return Response(response, status=404)

    def delete(self, request, note_id):
        """
        :param request:  data is requested
        :param note_id:  note id
        :return: will fetch note id from database
        """
        smd = {'success': False, 'message': 'not a vaild note id ', 'data': []}
        try:
            note = get_object_or_404(Notes, id=note_id)
            note.is_trashed = True  # is_deleted, is_removed, is_trashed
            note.save()
            logger.info("note with node_id :%s was trashed for user :%s", note_id, request.user)
            smd = {'success': True, 'message': 'note is deleted ', 'data': []}
            return HttpResponse(json.dumps(smd, indent=2), status=201)
        except KeyError:
            logger.info("note with node_id :%s was already deleted for user :%s", note_id, request.user)
            return HttpResponse(json.dumps(smd, indent=2), status=404)
        except Exception as e:
            logger.info("note with node_id :%s was already deleted for user :%s", note_id, request.user)
            response = {'success': False, 'message': str(e), 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=404)


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
            redis_data = red.hmget(user.id + "label")
            if redis_data is None:
                labels = Label.objects.filter(user_id=user.id)
                label_name = [i.name for i in labels]
                logger.info("labels where fetched from database for user :%s", request.user)
                return Response(label_name, status=200)
            logger.info("labels where fetched from redis for user :%s", request.user)
            return Response(redis_data, status=200)
        except Exception:
            logger.error("labels where not fetched for user :%s", request.user)
            return Response(response, status=400)

    def post(self, request):
        """
        :param request: request from user
        :return: will get all lables created by user
        """
        user = request.user
        response = {"success": False, "message": "something went wrong", "data": []}
        try:
            label = request.data["name"]
            if Label.objects.filter(user_id=user.id, name=label).exists():
                logger.info("label is already exists for %s", user)
                response['message'] = "note is already exists"
                # response = {"success": False, "message": "note is already exists", "data": label}
                return Response(response, status=400)

            label_created = Label.objects.create(user_id=user.id, name=label)
            red.hmset(user.id + "label", {label_created.id: label})
            logger.info("note is created for %s", user)
            response = {"success": True, "message": "note is created", "data": label}
            return Response(response, status=201)
        except Exception as e:
            logger.error("%s while creating note for %s", str(e), user)
            return Response(response, status=404)


# @method_decorator(login_decorator, name='dispatch')
class LabelsUpdate(GenericAPIView):
    serializer_class = LabelSerializer

    # permission_classes = (IsAuthenticated,)

    def put(self, request, label_id):
        """
        :param label_id: id of the label
        :param request: request from user
        :return: will update the data
        """
        response = {
            "success": False,
            "message": "Something bad happened",
            "data": []
        }
        user = request.user
        try:
            requestBody = json.loads(request.body)
            label_name = requestBody['name']
            label_updated = Label.objects.get(id=label_id, user_id=user.id)
            label_updated.name = label_name
            label_updated.save()
            red.hmset(user.id + "label", {label_updated.id: label_id})
            response["message"] = "label updated successfully"
            response["data"] = [label_name]
            response["success"] = True
            logger.info("label was updated for %s",user)
            return HttpResponse(json.dumps(response, indent=2), status=200)
        except KeyError as k:
            logger.error("error:%s while creating label for %s", str(k), user)
            response["message"] = "label does not exist"
            return Response(response, status=400)
        except Exception as e:
            logger.error("error:%s while creating label for %s", str(e), user)
            return Response(response, status=404)

    def delete(self, request, label_id):
        """
        :param request: request from user
        :param label_id: name of the label
        :return: will delete the data
        """
        response = {
            "success": False,
            "message": "Something bad happened",
            "data": []
        }
        user = request.user
        try:
            label_id = Label.objects.get(id=label_id, user_id=[user.id, ])
            label_id.delete()
            red.hdel(user.id + "label", label_id)
            logger.info("label is deleted for %s", user)
            response = {"success": True, "message": "label is deleted", "data": []}
            return Response(response, status=204)
        except Exception as e:
            logger.info("got error : %s while deleting label for  %s", str(e), user)
            return Response(response, status=404)


@method_decorator(login_decorator, name='dispatch')
class Archive(GenericAPIView):
    # serializer_class = ArchiveSerializer

    def get(self, request):
        response = {"success": False, "message": "something went wrong", "data": []}
        user = request.user
        try:
            response = {"success": True, "message": "Your archived notes will appear here"}
            no = Notes.objects.filter(user_id=user.id, is_archive=True)
            if len(no) is None:
                logger.info("zero archived notes fetched for %s", user)
                return HttpResponse(json.dumps(response), status=200)
            logger.info("archive data is loaded for %s", user)
            return HttpResponse(no.values(), status=200)
        except Exception as e:
            logger.error(" error: %e  for %s while fetching archive notes", user, str(e))
            return HttpResponse(json.dumps(response), status=404)


@method_decorator(login_decorator, name='dispatch')
class Trash(GenericAPIView):
    # serializer_class = ArchiveSerializer

    def get(self, request):
        response = {"success": False, "message": "something went wrong", "data": []}
        user = request.user
        try:
            user = request.user
            no = Notes.objects.filter(user_id=user.id, is_trashed=True)
            if len(no) is None:
                logger.info("No notes in Trash for %s", user)
                response = {"success": True, "message": "No notes in Trash "}
                return HttpResponse(json.dumps(response), status=200)
            logger.info("Trash data is loaded for %s",user)
            return HttpResponse(no.values())
        except Exception as e:
            logger.error("error:%e for %s while fetching trashed notes", user, str(e))
            HttpResponse(json.dumps(response, status=404))


@method_decorator(login_decorator, name='dispatch')
class Reminders(GenericAPIView):

    def get(self, request):
        # pdb.set_trace()
        user = request.user
        try:
            reminder_data = Notes.objects.filter(user_id=user.id)
            reminder_list = reminder_data.values_list('reminder', flat=True)
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

            logger.info("Reminders data is loaded for %s", user)
            return HttpResponse(reminder.values(), status=200)
        except TypeError as e:
            logger.error("error: %s for %s while fetching reminder page", str(e), user)
            smd = {"success": False, "message": "no reminder set", 'data': []}
            return HttpResponse(json.dumps(smd), status=200)

        except Exception as e:
            logger.error("error: %s for %s while fetching reminder page", str(e), user)
            smd = {"success": False, "message": "no reminder set", 'data': []}
            return HttpResponse(json.dumps(smd), status=404)


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
                user = User.objects.get(pk=user.id)
                note_create = Notes(user_id=user.id, note=note, title=title)

                note_create.save()
                return redirect(TWITTER_PAGE + str(title) + "\n" + str(note))
        except (IntegrityError, Exception):
            return HttpResponse(json.dumps(smd, indent=2), status=400)


class LazyLoading(GenericAPIView):
    serializer_class = NotesSerializer

    def get(self, request):
        notes = Notes.objects.filter(user_id=request.user.id)
        return render(request, 'user/email.html', {'notes': notes.values()[:15]})


class Sns(GenericAPIView):
    serializer_class = NotesSerializer

    def get(self, request):
        return HttpResponse(json.dumps("decdcd"))
