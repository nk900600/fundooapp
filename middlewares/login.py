import json
import logging
import pdb
import re

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import path, include

from fundoo.settings import file_handler
from lib.redis import red

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


class LoginDecorator:
    def __init__(self, function):
        self.function = function
        # One-time configuration and initialization.

    def __call__(self, request , *args, **kwargs):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # pdb.set_trace()
        if re.match("/api/+\w",request.get_full_path()):
            if re.match("/api/token/",request.get_full_path()):
                return self.function(request, *args, **kwargs)
            response = {"success": False, "message": "please login again", 'data': []}

            try:
                if request.META["HTTP_AUTHORIZATION"]:
                    try:
                        header = request.META["HTTP_AUTHORIZATION"]
                        token = header.split(" ")
                        decode = jwt.decode(token[1], settings.SECRET_KEY)
                        user = User.objects.get(id=decode['user_id'])
                        if red.get(user.username) is None:
                            logger.error("user credential were not found in redis ")
                            response['message'] = "something went wrong please login back"
                            return HttpResponse(json.dumps(response, indent=2), status=404)
                        logger.info("%s logged in using simple jwt", user.username)
                        return self.function(request, *args, **kwargs)
                    except jwt.exceptions.DecodeError as e:
                        response["message"] = str(e)
                        logger.error("token decode error")
                        return HttpResponse(json.dumps(response, indent=2), status=404)
                    except jwt.exceptions.ExpiredSignatureError as e:
                        logger.error("token expired ")
                        response['message'] = str(e)
                        return HttpResponse(json.dumps(response, indent=2), status=404)
                    except User.DoesNotExist as e:
                        logger.error("token decode user id doesnt exist")
                        response["message"] = str(e)
                        return HttpResponse(json.dumps(response, indent=2), status=404)
            except KeyError:
                pass

            if request.COOKIES.get(settings.SESSION_COOKIE_NAME) is None:
                logger.error("session_id not present or expired")
                response = {"success": False, "message": "something went wrong please login again", 'data': []}
                return HttpResponse(json.dumps(response, indent=2), status=404)
            else:
                logger.info("%s logged in using social login ", request.user)
                return self.function(request, *args, **kwargs)
        else:

            return self.function(request, *args, **kwargs)
