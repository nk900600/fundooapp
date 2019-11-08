import json
import logging
import pdb
from pdb import set_trace

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, get_object_or_404
#
# from note.views import collvalidator, labelvalidator
from jwt import DecodeError, InvalidTokenError
from rest_framework_simplejwt.exceptions import InvalidToken

from fundoo.settings import file_handler
from note.models import Label, Notes
from lib.redis import red
from django.core import signing
from pymitter import EventEmitter
# from django.urls import reverse
#
# current_url = reverse(request.path_info).url_name
ee = EventEmitter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def redirect_after_login(function):
    """
    :param function: function is called
    :return: will check token expiration
    """

    def wrapper(request, *args, **kwargs):
        """
        :return: will check token expiration
        """
        user = request.user
        if user.id is not None:
            logger.info("user already logged ")
            return redirect("/api/note")
        return function(request, *args, **kwargs)

    return wrapper


def login_decorator(function):
    """
    :param function: function is called
    :return: will check token expiration
    """

    def wrapper(request, *args, **kwargs):
        """
        :return: will check token expiration
        """
        smd = {"success": False, "message": "please login again", 'data': []}
        try:
            # pdb=set_trace
            print(request.user)
            if request.COOKIES.get(settings.SESSION_COOKIE_NAME) or request.user:
                user = request.COOKIES.get(settings.SESSION_COOKIE_NAME)

                if user:
                    logger.info("%s logged in using session login", request.user)
                    return function(request, *args, **kwargs)
                else:
                    return HttpResponse(json.dumps(smd))
            else:
                header = request.META["HTTP_AUTHORIZATION"]
                token = header.split(" ")
                decode = jwt.decode(token[1], settings.SECRET_KEY)
                user = User.objects.get(id=decode['user_id'])
                red.get(user.username)
                logger.info("%s logged in using simple jwt", user.username)
                return function(request, *args, **kwargs)
        except KeyError as e:
            logger.error("please login again")
            return HttpResponse(json.dumps(smd, indent=2), status=404)

    return wrapper


# def label_coll_validator_post(function):
#     """
#     :param function: function is called
#     :return: will check token expiration
#     """
#
#     def wrapper(request):
#         try:
#             if labelvalidator(request.data['label'], request.user.id):
#                 smd = {'success': False, 'message': 'label is not created by this user or user does not exist',
#                        'data': []}
#                 return HttpResponse(json.dumps(smd, indent=2), status=400)
#         except KeyError:
#             pass
#         try:
#             # pdb.set_trace()
#             if collvalidator(request.data['collaborators']):
#                 smd = {'success': False, 'message': 'email not vaild',
#                        'data': []}
#                 return HttpResponse(json.dumps(smd, indent=2), status=400)
#         except KeyError:
#             pass
#
#         return function(request)
#
#     return wrapper


class LabelCollaborators:
    def __init__(self, function):
        self.function = function
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.get_full_path()=="/api/notes/":

            try:
                print(request.get_full_path())
                z=json.loads(request.body)

                if labelvalidator(z['label'], request.user.id):
                    smd = {'success': False, 'message': 'label is not created by this user or user does not exist',
                           'data': []}
                    return HttpResponse(json.dumps(smd, indent=2), status=400)
            except KeyError:
                pass
            try:
                # pdb.set_trace()
                if collvalidator(request.body):
                    smd = {'success': False, 'message': 'email not vaild',
                           'data': []}
                    return HttpResponse(json.dumps(smd, indent=2), status=400)
            except KeyError:
                pass

            response = self.function(request)
            return response
        else:
            pass
        # Code to be executed for each request/response after
        # the view is called.




def label_coll_validator_put(function):
    """
    :param function: function is called
    :return: will check token expiration
    """

    def wrapper(request, note_id):
        user = request.user
        try:
            label = request.data['label']

            if labelvalidator(label, user.id):
                smd = {'success': False, 'message': 'label is not created by this user or user does not exist',
                       'data': []}
                return HttpResponse(json.dumps(smd, indent=2), status=400)
        except KeyError:
            pass

        try:
            collaborators = request.data['collaborators']
            if collvalidator(collaborators):
                smd = {'success': False, 'message': 'email not vaild',
                       'data': []}
                return HttpResponse(json.dumps(smd, indent=2), status=400)
        except KeyError:
            pass
        return function(request, note_id)

    return wrapper


def labelvalidator(label, user_id):
    """
    :param label: label is taken
    :param user_id: userid is formed
    :return: will return results
    """
    lab = []
    try:
        # pdb.set_trace()
        ll = Label.objects.filter(user_id=user_id)
        for i in range(len(label)):
            get_object_or_404(Label, name=label[i], user_id=user_id)
            lab.append(ll.values()[i]["name"])

        return False
    except Exception:
        logger.error("%s was not found under %s  ", label, user_id)
        return True


def collvalidator(collaborators):
    """
    :param collaborators: email is fetched
    :return: will return true or false
    """
    try:
        for email in collaborators:
            email_id = User.objects.filter(email=email)
            id = email_id.values()[0]['id']
        return False
    except Exception:
        logger.error(" %s does not exist", collaborators)
        return True
