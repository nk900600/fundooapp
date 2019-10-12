import json
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from services.redis import Redis
from django.core import signing


def login_decorator(function):
    """
    :param function: function is called
    :return: will check token expiration
    """
    def wrapper(request):
        """
        :return: will check token expiration
        """
        smd = {"success": False, "message": "not a vaild user", 'data': []}
        try:

            if request.COOKIES.get(settings.SESSION_COOKIE_NAME):
                user = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
                if user:
                    return function(request)
                else:
                    return HttpResponse(json.dumps(smd))
            else:
                header = request.META["HTTP_AUTHORIZATION"]
                token = header.split(" ")
                decode = jwt.decode(token[1], settings.SECRET_KEY)
                user = User.objects.get(id=decode['user_id'])
                red = Redis() # red object is created
                red.get(user.username)
                return function(request)

        except (Exception,TypeError):
            return HttpResponse(json.dumps(smd))
    return wrapper



