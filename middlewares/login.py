import json
import logging

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
        # url = [
        #     path("api/", include('note.url'))]

        # if url:

        smd = {"success": False, "message": "please login again", 'data': []}
        try:
            # pdb=set_trace

            if request.COOKIES.get(settings.SESSION_COOKIE_NAME) or request.user:
                user = request.COOKIES.get(settings.SESSION_COOKIE_NAME)

                if user:
                    logger.info("%s logged in using session login", request.user)
                    return self.function(request, *args, **kwargs)
                else:
                    return HttpResponse(json.dumps(smd))
            else:
                header = request.META["HTTP_AUTHORIZATION"]
                token = header.split(" ")
                decode = jwt.decode(token[1], settings.SECRET_KEY)
                user = User.objects.get(id=decode['user_id'])
                red.get(user.username)
                logger.info("%s logged in using simple jwt", user.username)
                return self.function(request, *args, **kwargs)

        except KeyError as e:
            logger.error("please login again")
            # return HttpResponse(json.dumps(smd, indent=2), status=404)

        # return response
        # else:
        #     response = self.function(request)
