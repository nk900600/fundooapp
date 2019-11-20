"""
 ******************************************************************************
 *  Purpose: note app is created so all the note CRUD and label CRUD is created,
 *           user can create, update ,delete or search note or label
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   30/09/2019
 ******************************************************************************
"""

import json

import requests
from oauthlib.oauth2 import BackendApplicationClient
from datetime import datetime, timedelta
from functools import wraps
from django.utils import timezone
import django
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template.loader import render_to_string
from django.utils import timezone as tz
from django.shortcuts import get_object_or_404, render
import redis
import pdb
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fundoo.settings import PORT, DB, file_handler, TWITTER_PAGE, logging, SOCIAL_AUTH_GITHUB_KEY, \
    SOCIAL_AUTH_GITHUB_SECRET
from note.documents import NotesDocument
from note.serialized import NotesSerializer, UpdateSerializer, ShareSerializer, LabelSerializer, \
    NotesDocumentSerializer  # ArchiveSerializer
from lib.amazones3 import AmazoneS3
from note.decorators import login_decorator, label_coll_validator_put  # , label_coll_validator_post
from lib.redis import red
# import logging
from .models import Notes, Label
from pymitter import EventEmitter

ee = EventEmitter()
s3 = AmazoneS3()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


@method_decorator(login_decorator, name='dispatch')
class NoteCreate(GenericAPIView):
    """
        Summary:
        --------
            Note class will let authorized user to create and get notes.

        Methods:
        --------
            get: User will get all the notes.
            post: User will able to create new note.

    """
    serializer_class = NotesSerializer

    def get(self, request):
        """
           Summary:
           --------
                All the notes will be fetched for the user.

           Exception:
           ----------
               PageNotAnInteger: object
               EmptyPage: object

           Returns:
           --------
               Html_page: pagination.html    Jinja-arg=['notes']
        """
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
        return render(request, 'user/pagination.html', {'notes': notes}, status=200)

    # parser_classes = (FormParser,FileUploadParser)
    @staticmethod
    def post(request):
        """
             Summary:
             --------
                 New note will be create by the User.

             Exception:
             ----------
                 KeyError: object

             Returns:
             --------
                 response: SMD format of note create message or with error message
        """

        user = request.user
        try:
            # data is taken from user
            # pdb.set_trace()
            data = request.data
            if len(data) == 0:
                raise KeyError
            user = request.user
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
            if serializer.is_valid():
                note_create = serializer.save(user_id=user.id)
                response = {'success': True, 'message': "note created", 'data': []}
                if serializer.data['is_archive']:
                    red.hmset(str(user.id) + "is_archive",
                              {note_create.id: str(json.dumps(serializer.data))})  # created note is cached in redis
                    logger.info("note is created for %s with note id as %s", user, note_create.id)
                    return HttpResponse(json.dumps(response, indent=2), status=201)
                else:
                    if serializer.data['reminder']:
                        red.hmset("reminder",
                                  {note_create.id: str(json.dumps({"email": user.email, "user": str(user),
                                                                   "note_id": note_create.id,
                                                                   "reminder": serializer.data["reminder"]}))})
                    red.hmset(str(user.id) + "note",
                              {note_create.id: str(json.dumps(serializer.data))})

                    logger.info("note is created for %s with note data as %s", user, note_create.__repr__())
                    return HttpResponse(json.dumps(response, indent=2), status=201)
            logger.error(" %s for  %s", user, serializer.errors)
            response = {'success': False, 'message': "note was not created", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=400)
        except KeyError as e:
            print(e)
            logger.error("got %s error for creating note as no data was provided for user %s", str(e), user)
            response = {'success': False, 'message': "one of the field is empty ", 'data': []}
            return Response(response, status=400)
        except Exception as e:
            print(e)
            logger.error("got %s error for creating note for user %s", str(e), user)
            response = {'success': False, 'message': "something went wrong", 'data': []}
            return Response(response, status=400)


@method_decorator(login_decorator, name='dispatch')
class NoteUpdate(GenericAPIView):
    """
        Summary:
        --------
             Note update class will let authorized user to update and delete note.

        Methods:
        --------
            get: User will get particular note which he want.
            put: User will able to update existing note.
            delete: User will able to delete  note.

    """
    serializer_class = UpdateSerializer

    @staticmethod
    def get(request, note_id):
        """
              Summary:
              --------
                  Note will be fetched by the User.

              Exception:
              ----------
                  Notes.DoesNotExist: object

              Returns:
              --------
                  response: will return all the note data or will return
                            error msg if note id does not exist
        """
        try:
            # pdb.set_trace()
            redis_data = red.hmget(str(request.user.id) + "note", str(note_id))
            user = request.user
            if redis_data == [None]:
                note = Notes.objects.filter(id=note_id)
                serialized_data = NotesSerializer(note, many=True)
                logger.info("note was fetched from database for user %s", user)
                return HttpResponse(json.dumps(serialized_data.data, indent=1), status=200)

            logger.info("note was fetched form redis for user %s", user)
            return HttpResponse(redis_data, status=200)
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
          Summary:
          --------
              Note will be updated by the User.

          Exception:
          ----------
              Keyerror: object

          Returns:
          --------
              response: will return updated note or will return error with smd format
        """
        user = request.user
        try:
            # pdb.set_trace()
            # data is fetched from user
            instance = Notes.objects.get(id=note_id)
            data = request.data
            if len(data) == 0:
                raise KeyError
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
            serializer = UpdateSerializer(instance, data=data, partial=True)
            # here serialized data checked for validation and saved
            if serializer.is_valid():
                note_create = serializer.save()
                response = {'success': True, 'message': "note updated", 'data': [serializer.data]}
                print(serializer.data)
                # pdb.set_trace()
                if serializer.data['is_archive']:
                    red.hmset(str(user.id) + "is_archive",
                              {note_create.id: str(json.dumps(serializer.data))})
                    logger.info("note was updated with note id :%s for user :%s ", note_id, user)
                    return HttpResponse(json.dumps(response, indent=2), status=200)
                elif serializer.data['is_trashed']:
                    red.hmset(str(user.id) + "is_trashed",
                              {note_create.id: str(json.dumps(serializer.data))})
                    logger.info("note was updated with note id :%s for user :%s ", note_id, user)
                    return HttpResponse(json.dumps(response, indent=2), status=200)
                else:
                    if serializer.data['reminder']:
                        red.hmset("reminder",
                                  {note_create.id: str(json.dumps({"email": user.email, "user": str(user),
                                                                   "note_id": note_create.id,
                                                                   "reminder": serializer.data["reminder"]}))})

                    red.hmset(str(user.id) + "note",
                              {note_create.id: str(json.dumps(serializer.data))})
                    logger.info("note was updated with note id :%s for user :%s ", note_id, user)
                    return HttpResponse(json.dumps(response, indent=2), status=200)
            logger.error("note was updated with note id :%s for user :%s ", note_id, user)
            response = {'success': False, 'message': "note was not created", 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=400)
        except KeyError as e:
            print(e)
            logger.error("no data was provided from user %s to update", str(e), user)
            response = {'success': False, 'message': "note already upto data ", 'data': []}
            return Response(response, status=400)
        except Exception as e:
            logger.error("got error :%s for user :%s while updating note id :%s", str(e), user, note_id)
            response = {'success': False, 'message': str(e), 'data': []}
            return Response(response, status=404)

    def delete(self, request, note_id, *args, **kwargs):
        """
          Summary:
          --------
              Note will be deleted by the User.

          Exception:
          ----------
              Keyerror: object

          Returns:
          --------
              response: will return SMD format of deleted note or with error message
        """

        smd = {'success': False, 'message': 'not a vaild note id ', 'data': []}
        user = request.user
        try:
            # pdb.set_trace()
            note = Notes.objects.get(id=note_id)
            note.is_trashed = True  # is_deleted, is_removed, is_trashed
            note.save()
            note_data = Notes.objects.filter(id=note_id)
            serialized_data = NotesSerializer(note_data, many=True)

            red.hmset(str(user.id) + "is_trashed",
                      {note.id: str(json.dumps(serialized_data.data))})
            red.hdel(str(user.id) + "note", note_id)
            logger.info("note with node_id :%s was trashed for user :%s", note_id, request.user)
            smd = {'success': True, 'message': 'note is deleted ', 'data': []}
            return HttpResponse(json.dumps(smd, indent=2), status=status.HTTP_201_CREATED)
        except KeyError:
            logger.info("note with node_id :%s was already deleted for user :%s", note_id, request.user)
            return HttpResponse(json.dumps(smd, indent=2), status=404)
        except Exception as e:
            logger.info("note with node_id :%s was already deleted for user :%s", note_id, request.user)
            response = {'success': False, 'message': str(e), 'data': []}
            return HttpResponse(json.dumps(response, indent=2), status=404)


@method_decorator(login_decorator, name='dispatch')
class LabelsCreate(GenericAPIView):
    """
        Summary:
        --------
             Label create class will let authorized user to get and create label.

        Methods:
        --------
            get: User will get all the created labels by the  user.
            post: User will able to create more labels.

    """
    serializer_class = LabelSerializer

    def get(self, request):
        """
          Summary:
          --------
              label will be fetched by the User.

          Exception:
          ----------
              Exception:  if anything goes wrong.

          Returns:
          --------
              response:  User will get all the created labels by the user or
                        error msg if label id does not exist.
        """
        response = {
            "success": False,
            "message": "something went wrong",
            "data": []
        }
        try:
            # pdb.set_trace()
            user = request.user
            redis_data = red.hvals(str(user.id) + "label")
            if len(redis_data) == 0:
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
          Summary:
          --------
              label will be created by the User.

          Exception:
          ----------
              Exception:  if anything goes wrong.

          Returns:
          --------
              response:  User will able to create labels  or
                        error msg will be returned if something goes wrong.
        """
        # pdb.set_trace()
        user = request.user
        response = {"success": False, "message": "something went wrong", "data": []}
        try:

            label = request.data["name"]
            if label == "":
                logger.info("label input was not given for %s", user)
                response['message'] = "no input"
                return Response(response, status=400)

            if Label.objects.filter(user_id=user.id, name=label).exists():
                logger.info("label is already exists for %s", user)
                response['message'] = "label is already exists"
                return Response(response, status=400)

            label_created = Label.objects.create(user_id=user.id, name=label)
            red.hmset(str(user.id) + "label", {label_created.id: label})
            logger.info("label is created for %s", user)
            response = {"success": True, "message": "label is created", "data": label}
            return HttpResponse(json.dumps(response), status=201)
        except Exception as e:
            logger.error("%s while creating label for %s", str(e), user)
            return Response(response, status=404)


@method_decorator(login_decorator, name='dispatch')
class LabelsUpdate(GenericAPIView):
    """
       Summary:
       --------
            Label update class will let authorized user to update or delete label.

       Methods:
       --------
           put: User will be able to update label.
           delete: User will able to delete one or more labels.

    """
    serializer_class = LabelSerializer

    def put(self, request, label_id):
        """
            Summary:
            --------
                label will be updated by the User.

            Exception:
            ----------
                Exception:  if anything goes wrong.

            Returns:
            --------
                response:  User will able to updated label or error msg if something goes wrong
        """
        response = {
            "success": False,
            "message": "Something bad happened",
            "data": []
        }
        user = request.user
        try:
            # pdb.set_trace()
            requestBody = json.loads(request.body)
            label_name = requestBody['name']
            label_updated = Label.objects.get(id=label_id, user_id=user.id)
            label_updated.name = label_name
            label_updated.save()
            red.hmset(str(user.id) + "label", {label_updated.id: label_name})

            response["message"] = "label updated successfully"
            response["data"] = [label_name]
            response["success"] = True
            logger.info("label was updated for %s both on redis and database ", user)
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
            Summary:
            --------
                label will be deleted by the User.

            Exception:
            ----------
                Exception:  if anything goes wrong.

            Returns:
            --------
                response:  User will able to delete label or error msg if something goes wrong
        """
        response = {
            "success": False,
            "message": "label does not exist ",
            "data": []
        }
        user = request.user
        try:
            red.hdel(str(user.id) + "label", label_id)
            label_id = Label.objects.get(id=label_id, user_id=user.id)
            label_id.delete()
            logger.info("label is deleted for %s", user)
            response = {"success": True, "message": "label is deleted", "data": []}
            return Response(response, status=204)
        except Exception as e:
            logger.info("got error : %s while deleting label for  %s", str(e), user)
            return Response(response, status=404)


@method_decorator(login_decorator, name='dispatch')
class Archive(GenericAPIView):
    """
       Summary:
       --------
            Archive class will let authorized user to get archive notes.

       Methods:
       --------
           get: User will be able to get all archive notes.
    """

    def get(self, request):
        response = {"success": False, "message": "something went wrong", "data": []}
        user = request.user
        redis_data = red.hvals(str(user.id) + "is_archive")
        try:
            if len(redis_data) == 0:
                response = {"success": True, "message": "Your archived notes will appear here", "data": []}
                no = Notes.objects.filter(user_id=user.id, is_archive=True)
                if len(no) == 0:
                    logger.info("zero archived notes fetched for %s", user)
                    return HttpResponse(json.dumps(response), status=200)
                else:
                    logger.info("archive data is loaded for %s from database", user)
                    return HttpResponse(no.values(), status=200)
            logger.info("archive data is loaded for %s from redis", user)
            return HttpResponse(redis_data, status=200)
        except Exception as e:
            logger.error(" error: %e  for %s while fetching archive notes", user, str(e))
            return HttpResponse(json.dumps(response), status=404)


@method_decorator(login_decorator, name='dispatch')
class Trash(GenericAPIView):
    """
       Summary:
       --------
            Trash class will let authorized user to get Trashed notes.

       Methods:
       --------
           get: User will be able to get all trashed notes.
    """

    def get(self, request):
        response = {"success": False, "message": "something went wrong", "data": []}
        user = request.user
        # pdb.set_trace()
        try:
            redis_data = red.hvals(str(user.id) + "is_trashed")
            if len(redis_data) == 0:
                user = request.user
                no = Notes.objects.filter(user_id=user.id, is_trashed=True)
                if len(no) == 0:
                    logger.info("No notes in Trash for %s", user)
                    response = {"success": True, "message": "No notes in Trash "}
                    return HttpResponse(json.dumps(response), status=200)
                logger.info("Trash data is loaded for %s from database", user)
                return HttpResponse(no.values())
            logger.info("Trash data is loaded for %s from redis", user)
            return HttpResponse(redis_data)
        except Exception as e:
            logger.error("error:%e for %s while fetching trashed notes", user, str(e))
            HttpResponse(json.dumps(response, status=404))


@method_decorator(login_decorator, name='dispatch')
class Reminders(GenericAPIView):
    """
       Summary:
       --------
            Reminder class will let authorized user to get reminder notes.

       Methods:
       --------
           get: User will be able to get all reminder notes with fired and upcoming reminder.
                for upcoming reminder email will be set to user email address.
    """

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


class Celery(GenericAPIView):
    serializer_class = NotesSerializer
    """
      Summary:
      --------
           Celery class works on clery beat and every 1 min this end point is hit.

      Methods:
      --------
          get: this method where logic is written for triggering reminders notification service where 
               email is sent if reminder time matched with current time. 
    """

    def get(self, request):
        reminder_data = Notes.objects.filter(reminder__isnull=False)
        start = timezone.now()
        end = timezone.now() + timedelta(minutes=1)
        for i in range(len(reminder_data)):
            if start < reminder_data.values()[i]["reminder"] < end:
                user_id = reminder_data.values()[i]['user_id']
                user = User.objects.get(id=user_id)
                mail_message = render_to_string('user/email_reminder.html', {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'note_id': reminder_data.values()[i]["user_id"]
                })
                ee.emit(user.email, mail_message)
                logger.info("email is trigged for %s beacuse reminder was set for the user ", request.user)
        return HttpResponse(reminder_data)


@method_decorator(login_decorator, name='dispatch')
class SearchEngine(GenericAPIView):
    """
      Summary:
      --------
           Search engine class is a api where user can search notes on basis's of
            note or title or reminder or email as per user.

      Methods:
      --------
          post: input is taken from the user and search result is given out
    """

    serializer_class = NotesDocumentSerializer

    def post(self, request):
        response = {"success": False, "message": "something went wrong", "data": []}
        try:
            user_input = request.data['title']
            note = NotesDocument.search().query({
                "bool": {
                    "must": [
                        {"multi_match": {
                            "query": user_input,
                            "fields": ["label.name", 'title', 'note', 'reminder', 'color', 'user.email']
                        }},
                    ],
                    "filter": [
                        {"term": {"user.username": str(request.user)}}
                    ]
                }
            })
            note_data = NotesSerializer(note.to_queryset(), many=True)
            logger.info("note were searched for the %s using elastic search", request.user)
            return HttpResponse(json.dumps(note_data.data, indent=2), status=200)
        except Exception as e:
            logger.error("error: %s for %s while searching vis elasticsearch", str(e), request.user)
            return HttpResponse(json.dumps(response, indent=2), status=400)


@method_decorator(login_decorator, name='dispatch')
class NoteShare(GenericAPIView):

    serializer_class = ShareSerializer

    def post(self, request):
        """
        :param request:  request from user
        :return:  will save note details posted by user
        """
        smd = {'success': False, 'message': 'not a valid note ', 'data': []}
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


# class LazyLoading(GenericAPIView):
#     serializer_class = NotesSerializer
#
#     def get(self, request):
#         notes = Notes.objects.get(id=81)
#
#         return render(request, 'user/email.html', {'notes': notes.color})
