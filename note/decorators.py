import json
import logging
from pdb import set_trace

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, get_object_or_404
#
# from note.views import collvalidator, labelvalidator
from fundoo.settings import file_handler
from note.models import Label, Notes
from lib.redis import red
from django.core import signing
from pymitter import EventEmitter
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
        smd = {"success": False, "message": "not a vaild user", 'data': []}
        try:
            # pdb=set_trace

            if request.COOKIES.get(settings.SESSION_COOKIE_NAME):
                user = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
                if user:
                    return function(request, *args, **kwargs)
                else:
                    return HttpResponse(json.dumps(smd))
            else:
                header = request.META["HTTP_AUTHORIZATION"]
                token = header.split(" ")
                decode = jwt.decode(token[1], settings.SECRET_KEY)
                user = User.objects.get(id=decode['user_id'])
                red.get(user.username)
                return function(request, *args, **kwargs)

        except Exception as e:
            print(e)
            # if TypeError:
            #     logger.error("typeerror as note query does not match ")
            #     smd = {"success": False, "message": "query does not match", 'data': []}
            #     return HttpResponse(json.dumps(smd, indent=2), status=400)
            # else:
            logger.error("broad exceptions as user is not logged in ")
            return HttpResponse(json.dumps(smd, indent=2), status=400)

    return wrapper


def label_coll_validator_post(function):
    """
    :param function: function is called
    :return: will check token expiration
    """

    def wrapper(request):
        user = request.user
        try:
            label = request.data['label']
            if labelvalidator(label, user.id):
                smd = {'success': False, 'message': 'label is not created by this user or user does not exist',
                       'data': []}
                return HttpResponse(json.dumps(smd, indent=2), status=400)
        except KeyError:
            logger.warning("keyerror as label was not added added")
            pass

        try:
            collaborators = request.data['collaborators']
            if collvalidator(collaborators):
                smd = {'success': False, 'message': 'email not vaild',
                       'data': []}
                return HttpResponse(json.dumps(smd, indent=2), status=400)
        except KeyError:
            logger.warning("keyerror as collaborators was not added added")
            pass

        return function(request)

    return wrapper


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
            logger.warning("keyerror as label was not added added")
            pass

        try:
            collaborators = request.data['coll']
            if collvalidator(collaborators):
                smd = {'success': False, 'message': 'email not vaild',
                       'data': []}
                return HttpResponse(json.dumps(smd, indent=2), status=400)
        except KeyError:
            logger.warning("keyerror as collaborators was not added added")
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
        logger.error("label was not found ")
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
    except Exception:
        logger.error(" collaborators does not exist")
        return True
