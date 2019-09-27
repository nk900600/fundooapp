import jwt,re
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def login_decorator(function):
    """
    :param function: function is called
    :return: will check token expiration
    """
    permission_classes = (IsAuthenticated,)

    def wrapper(request,*args, **kwargs):
        """
        :return: will check token expiration
        """
        username = request.user
        print(username)
        content = {'message': 'Hello, World!'}
        return function(request,*args, **kwargs)

        # return Response(content)
        # red = Redis() # red object is created
        # # token = red.get('token').decode("utf-8") # token is fetched from redis
        # print(token)
        # # try:
        # decode = jwt.decode(token, settings.SECRET_KEY)
        # # except TypeError:
        # #     return redirect('/session')
        # user1 = decode['username']
        # user2 = User.objects.get(username=user1)
        # if user2 is not None:
        #     print("hello")
        #     return function(request,*args, **kwargs)
        # # else:
        # # #     return redirect('/session')
        # else:
        #     return HttpResponse("hello")
    return wrapper



