"""
 ******************************************************************************
 *  Purpose: will save user details after registrations
 *
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   30/09/2019
 ******************************************************************************
"""

import json
from smtplib import SMTPAuthenticationError
import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from jwt import ExpiredSignatureError
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from services.token import token_activation, token_validation
from .serializer import RegistrationSerializer, UserSerializer, LoginSerializer, ResetSerializer, EmailSerializer
from django.core.validators import validate_email




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

    def get(self, request):
        return render(request, 'user/registration.html')

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
            return HttpResponse(json.dumps("please enter vaild email address"))
        # user input is checked
        if username == "" or email == "" or password == "":
            HttpResponse(json.dumps(smd))

        # if user exists it will show error message
        elif User.objects.filter(username=username).exists():
            HttpResponse(json.dumps(smd))

        # if email exists it will show error message
        elif User.objects.filter(email=email).exists():
            HttpResponse(json.dumps(smd))

        else:
            userCreated = User.objects.create_user(username=username, email=email, password=password,
                                                   is_active=False)
            userCreated.save()

            # user is unique then we will send token to his/her email for validation
            if userCreated is not None:

                token = token_activation(username, password)
                mail_subject = "Activate your account by clicking below link"
                mail_message = render_to_string('user/activatetoken.html', {
                    'user': userCreated.username,
                    'domain': get_current_site(request).domain,
                    'token': token
                })
                recipient_email = userCreated.email
                email = EmailMessage(mail_subject, mail_message, to=[recipient_email])
                try:
                    # email is sent from here with the url link
                    email.send()
                except SMTPAuthenticationError:
                    smd = {
                        'success': True,
                        'message': 'please check the mail and click on the link  for validation',
                        'data': [token],
                    }
                    return HttpResponse(json.dumps(smd))
                smd = {
                        'success': True,
                        'message': 'please check the mail and click on the link  for validation',
                        'data': [token],
                    } 
                return HttpResponse(json.dumps(smd))


class Login(GenericAPIView):
    """
    :param APIView: user request is made from the user
    :return: will check the credentials and will user
    """
    serializer_class = LoginSerializer

    def get(self, request):
        return render(request, 'user/login.html')

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
            HttpResponse(json.dumps(smd))
        user = auth.authenticate(username=username, password=password)
        # if user is not none then we will generate token
        if user is not None:
            token = token_validation(username, password)
            smd = {
                'success': True,
                'message': "successfully logged",
                'data': [token],
            }
            return HttpResponse(json.dumps(smd))
            # return redirect('/logout')
        else:
            return HttpResponse(json.dumps(smd))


# class Hello(GenericAPIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         return Response(json.dumps("hi"))


class Logout(GenericAPIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        :param request: logout request is made
        :return: we will delete the token which was stored in redis
        """
        # Authorization
        # print(request.META['HTTP_AUTHORIZATION'])
        print('hello')
        # return Response(json.dumps("hi"))
        return render(request,"user/logout.html")

    def post(self, request):
        """
        :param request: logout request is made
        :return: we will delete the token which was stored in redis
        """
        # Authorization
        # print(request.META['HTTP_AUTHORIZATION'])
        print('hello')
        return HttpResponse(json.dumps("hi"))
        # return render(request, "user/logout.html")


class ForgotPassword(GenericAPIView):
    """
    :param request: request is made for resetting password
    :return:  will return email where password reset link will be attached
    """
    serializer_class = EmailSerializer

    def get(self,request):
        return HttpResponse(json.dumps("hi"))

    def post(self,request):

        email = request.data["email"]
        smd = {
            'success': False,
            'message': "not a vaild email ",
            'data': []
        }
        # email validation is done here
        if email == "":
            return HttpResponse(json.dumps(smd))
        else:
            try:
                # i = 1
                # if i == 1:
                #     raise ValueError('my exception')
                try:
                    validate_email(email)
                except Exception:
                    HttpResponse(json.dumps(smd))

            
                user = User.objects.get(email=email)

                #  here user is not none then token is generated
                if user is not None:

                    token = token_activation(user.username,user.id)
                    # email is generated  where it is sent the email address entered in the form
                    mail_subject = "Activate your account by clicking below link"
                    mail_message = render_to_string('user/reset_password_token_link.html', {
                        'user': user.username,
                        'domain': get_current_site(request).domain,
                        'token': token
                    })
                    recipientemail = user.email
                    email = EmailMessage(mail_subject, mail_message, to=[recipientemail])
                    email.send()

                    smd = {
                        'success': True,
                        'message': "check email for vaildation ",
                        'data': []
                    }
                    # here email is sent to user
                    return HttpResponse(json.dumps(smd))
                # else:
                #     return HttpResponse(json.dumps(smd))
            except Exception as e:
                print(e)
                smd['message']= "not a registered user ",
                return HttpResponse(json.dumps(smd))




def activate(request, token):
    """
    :param request: request is made by the used
    :param token:  token is fetched from url
    :return: will register the account
    """
    try:
        # decode is done for the JWT token where username is fetched

        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then user account willed be activated
        if user is not None:
            user.is_active = True
            user.save()
            messages.info(request, "your account is active now")
            return redirect('/login')
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('/registration')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('/registration')
    except ExpiredSignatureError:
        messages.info(request, 'activation link expired')
        return redirect('/registration')


def reset_password(request, token):
    """
    :param request:  user will request for resetting password
    :param token: token is again send to the user
    :return: will reset the password
    """
    try:
        # here decode is done with jwt
        decode = jwt.decode(token, settings.SECRET_KEY)
        username = decode['username']
        user = User.objects.get(username=username)

        # if user is not none then we will fetch the data and redirect to the reset password page
        if user is not None:
            context = {'userReset': user.username}
            print(context)
            return redirect('/login/forgotpassword/resetpassword/' + str(user))
        else:
            messages.info(request, 'was not able to sent the email')
            return redirect('login/forgotpassword')
    except KeyError:
        messages.info(request, 'was not able to sent the email')
        return redirect('login/forgotpassword')
    except Exception:
        messages.info(request, 'activation link expired')
        return redirect('login/forgotpassword')


class ResetPassword(GenericAPIView):
    """
    :param user_reset: username is fetched
    :param request:  user will request for resetting password
    :return: will chnage the password
    """
    serializer_class = ResetSerializer

    def get(self, request, user_reset):
        try:
            User.objects.get(id=user_reset)
            return HttpResponse(json.dumps("hey user"))
        except Exception:
            return HttpResponse(json.dumps("not a vaild url"))

    def post(self, request, user_reset):

        password1 = request.data['password']
        # password2 = request.data['password']

        smd = {
            'success': False,
            'message': 'password reset not done',
            'data': [],
        }
        try:
            # password validation is done in this form
            if password1 == "" or password2 == "":
                return HttpResponse(json.dumps(smd))

            elif password2 != password1:
                return HttpResponse(json.dumps(smd))

            elif user_reset is None:
                return HttpResponse(json.dumps(smd))

            else:
                user = User.objects.get(username=user_reset)
                user.set_password(password1)
                # here we will save the user password in the database
                user.save()

                smd = {
                    'success': True,
                    'message': 'password reset done',
                    'data': [],
                }
                return HttpResponse(json.dumps(smd))
        except Exception:
            return HttpResponse(json.dumps(smd))


def session(request):
    """
    :param request: request is made
    :return:  if token is deleted and user goes back then it will take to user page
    """
    return render(request, 'user/session.html')
