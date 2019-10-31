"""
 ******************************************************************************
 *  Purpose: will save user details after registrations
 *
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   30/09/2019
 ******************************************************************************
"""
import datetime
import json
from smtplib import SMTPAuthenticationError

import django
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from jwt import ExpiredSignatureError
from pyee import BaseEventEmitter
from pymitter import EventEmitter
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
import pdb

from django.core.mail import EmailMultiAlternatives

from fundoo.settings import EMAIL_HOST_USER
from note.decorators import redirect_after_login
from lib.redis import red
from lib.emit_emitter import ee
from lib.token import token_activation, token_validation

from .serializer import RegistrationSerializer, UserSerializer, LoginSerializer, ResetSerializer, EmailSerializer
from django.core.validators import validate_email
from django_short_url.views import get_surl
from django_short_url.models import ShortURL


def home(request):
    """
    :param request: simple request is made from the user
    :return:
    """
    return render(request, 'user/index.html')


class Registrations(GenericAPIView):
    """
    :param request: request is made after filling the form
    :return: will send him the JWT token for validation
    """
    serializer_class = UserSerializer

    # def get(self, request):
    #     return render(request, 'user/registration.html')

    def post(self, request):

        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        smd = {
            'success': False,
            'message': "not registered yet",
            'data': [],
        }

        try:
            validate_email(email)
        except Exception:
            smd['message'] = "please enter vaild email address"
            return HttpResponse(json.dumps(smd), status=400)

        # user input is checked
        if username == "" or email == "" or password == "":
            smd['message'] = "one of the details missing"
            return HttpResponse(json.dumps(smd), status=400)

        # if email exists it will show error message
        elif User.objects.filter(email=email).exists():
            smd['message'] = "email address is already registered "
            return HttpResponse(json.dumps(smd), status=400)

        else:
            try:
                user_created = User.objects.create_user(username=username, email=email, password=password,
                                                        is_active=False)
                user_created.save()

                # user is unique then we will send token to his/her email for validation
                if user_created is not None:
                    token = token_activation(username, password)
                    url = str(token)
                    surl = get_surl(url)
                    z = surl.split("/")

                    mail_subject = "Activate your account by clicking below link"
                    mail_message = render_to_string('user/email_validation.html', {
                        'user': user_created.username,
                        'domain': get_current_site(request).domain,
                        'surl': z[2]
                    })
                    recipient_email = user_created.email
                    email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
                    email.send()
                    smd = {
                        'success': True,
                        'message': 'please check the mail and click on the link  for validation',
                        'data': [token],
                    }
                    return HttpResponse(json.dumps(smd), status=201)
            except Exception:
                smd["success"] = False
                smd["message"] = "username already taken"
                return HttpResponse(json.dumps(smd), status=400)


# @method_decorator(redirect_after_login, name='dispatch')
class Login(GenericAPIView):
    """
    :param APIView: user request is made from the user
    :return: will check the credentials and will user
    """
    serializer_class = LoginSerializer

    # def get(self,request):
    #     return render(request, 'user/login.html')

    # @xframe_options_deny
    @csrf_exempt
    def post(self, request):

        username = request.data['username']
        password = request.data['password']
        smd = {
            'success': False,
            'message': "not logged in ",
            'data': []
        }
        # validation is done
        if username == "" or password == "":
            smd['message'] = 'one or more fields is empty'
            return HttpResponse(json.dumps(smd), status=400)

        user = auth.authenticate(username=username, password=password)
        # if user is not none then we will generate token
        if user is not None:

            token = token_validation(username, password)

            # red = Redis()
            red.set(user.username, token)
            smd = {
                'success': True,
                'message': "successfully logged",
                'data': [token],
            }

            return HttpResponse(json.dumps(smd), status=201)

        else:
            smd['message'] = 'invaild credentials'
            return HttpResponse(json.dumps(smd), status=400)


class Logout(GenericAPIView):
    serializer_class = LoginSerializer

    def get(self, request):
        """
        :param request: logout request is made
        :return: we will delete the token which was stored in redis
        """
        smd = {"success": False, "message": "not a vaild user", "data": []}
        try:

            user = request.user
            # red = Redis()
            red.delete(user.username)
            smd = {"success": True, "message": " logged out", "data": []}
            return HttpResponse(json.dumps(smd), status=200)
        except Exception:
            return HttpResponse(json.dumps(smd), status=400)


class ForgotPassword(GenericAPIView):
    """
    :param request: request is made for resetting password
    :return:  will return email where password reset link will be attached
    """
    serializer_class = EmailSerializer

    # def get(self, request):
    #     return HttpResponse(json.dumps("hi"))

    # @csrf_protect
    def post(self, request):

        global response
        email = request.data["email"]
        response = {
            'success': False,
            'message': "not a vaild email ",
            'data': []
        }
        # email validation is done here

        if email == "":
            response['message'] = 'email field is empty please provide vaild input'
            return HttpResponse(json.dumps(response), status=400)
        else:

            try:
                validate_email(email)
            except Exception:
                return HttpResponse(json.dumps(response))
            try:
                # pdb.set_trace()
                user = User.objects.filter(email=email)
                useremail = user.values()[0]["email"]
                username = user.values()[0]["username"]
                id = user.values()[0]["id"]

                #  here user is not none then token is generated
                if useremail is not None:
                    token = token_activation(username, id)
                    url = str(token)
                    surl = get_surl(url)
                    z = surl.split("/")

                    # email is generated  where it is sent the email address entered in the form
                    mail_subject = "Activate your account by clicking below link"
                    mail_message = render_to_string('user/email_validation.html', {
                        'user': username,
                        'domain': get_current_site(request).domain,
                        'surl': z[2]
                    })

                    recipientemail = email

                    ee.emit('send_email', recipientemail, mail_message)

                    response = {
                        'success': True,
                        'message': "check email for vaildation ",
                        'data': []
                    }
                    # here email is sent to user
                    return HttpResponse(json.dumps(response), status=201)
            except Exception as e:
                print(e)
                response['message'] = "something went wrong"
                return HttpResponse(json.dumps(response), status=400)


def activate(request, surl):
    """
    :param request: request is made by the used
    :param token:  token is fetched from url
    :return: will register the account
    """
    try:
        # decode is done for the JWT token where username is fetched

        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then user account willed be activated
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, "your account is active now")
            return redirect('/api/login')
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('/api/registration')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('/api/registration')
    except ExpiredSignatureError:
        messages.info(request, 'activation link expired')
        return redirect('/api/registration')


def reset_password(request, surl):
    """
    :param surl:  token is again send to the user
    :param request:  user will request for resetting password
    :return: will reset the password
    """
    try:
        # here decode is done with jwt

        tokenobject = ShortURL.objects.get(surl=surl)
        token = tokenobject.lurl
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then we will fetch the data and redirect to the reset password page
        if user is not None:
            context = {'userReset': user.username}
            print(context)
            return redirect('/api/resetpassword/' + str(user))
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('/api/forgotpassword')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('/api/forgotpassword')
    except Exception as e:
        print(e)
        messages.info(request, 'activation link expired')
        return redirect('/api/forgotpassword')


class ResetPassword(GenericAPIView):
    """
    :param user_reset: username is fetched
    :param request:  user will request for resetting password
    :return: will chnage the password
    """
    serializer_class = ResetSerializer

    # @csrf_protect
    def post(self, request, user_reset):

        password1 = request.data['password']
        password2 = request.data['password']

        smd = {
            'success': False,
            'message': 'password reset not done',
            'data': [],
        }
        # password validation is done in this form
        if user_reset is None:
            smd['message'] = 'not a vaild user'
            return HttpResponse(json.dumps(smd), status=400)

        elif password1 == "" or password2 == "":
            smd['message'] = 'one of the fields are empty'
            return HttpResponse(json.dumps(smd), status=400)

        elif len(password1) <= 4 or len(password2) <= 4:
            smd['message'] = 'password should be 4 or  more than 4 character'
            return HttpResponse(json.dumps(smd), status=400)

        else:
            try:

                user = User.objects.get(username=user_reset)
                user.set_password(password1)
                # here we will save the user password in the database
                user.save()

                smd = {
                    'success': True,
                    'message': 'password reset done',
                    'data': [],
                }
                return HttpResponse(json.dumps(smd), status=201)
            except User.DoesNotExist:
                smd['message'] = 'not a vaild user '
                return HttpResponse(json.dumps(smd), status=400)


def session(request):
    """
    :param request: request is made
    :return:  if token is deleted and user goes back then it will take to user page
    """
    return render(request, 'user/session.html')
