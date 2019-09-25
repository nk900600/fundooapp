import json
import re
from smtplib import SMTPAuthenticationError
import jwt
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from jwt import ExpiredSignatureError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Registration, LoggedUser
from services.amazones3 import upload_file


def home(request):
    """
    :param request: simple request is made from the user
    :return:
    """
    return render(request, 'login/index.html')


class Registrations(APIView):
    """
    :param request: request is made after filling the form
    :return: will send him the JWT token for validation
    """
    @staticmethod
    def get(request):
        return render(request, 'login/registration.html')


    @staticmethod
    @csrf_exempt
    def post(request):
        print(request.method)
        # if request.method == 'POST':
        firstname = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        file = request.FILES.get('file')
        print(file)
        filename=str(username)+str(file)
        upload_file(file,filename)
        url="https://django-s3-files.s3.us-east-2.amazonaws.com/"+filename

        # user input is checked
        if firstname == "" or username == "" or email == "" or password == "":
            messages.info(request, "one of the above field is empty")
            return redirect('/registration')

        # if user exists it will show error message
        elif User.objects.filter(username=username).exists():
            messages.info(request, "user already exists")
            return redirect('/registration')

        # if email exists it will show error message
        elif User.objects.filter(email=email).exists():
            messages.info(request, "email already exists")
            return redirect('/registration')

        else:
            userSaved = Registration(username=username, email=email, password=password)
            userSaved.save()
            userCreated = User.objects.create_user(username=username, email=email, password=password,
                                                   first_name=firstname, is_active=False)
            userCreated.save()

            # user is unique then we will send token to his/her email for validation
            if userCreated is not None:
                data = {
                    'username': username,
                    'password': password
                }
                token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256").decode('utf-8')
                mail_subject = "Activate your account by clicking below link"
                mail_message = render_to_string('login/activatetoken.html', {
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
                    messages.info(request, "please enter vaild email address")
                    return redirect('/registration')

                messages.info(request, "please check your mail for the validation link ")
                return render(request,'login/s3testing.html', {'url': url})


class Login(APIView):
    """
    :param APIView: login request is made from the user
    :return: will check the credentials and will login
    """

    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']

        # validation is done
        if username == "" or password == "":
            messages.info(request, "one of the above field is empty")
            return redirect('/login')
        user = auth.authenticate(username=username, password=password)

        # if user is not none then we will generate token
        if user is not None:
            data = {
                'username': username,
                'password': password
            }
            # here token is created and data is stored in redis
            token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256").decode('utf-8')
            userlist = []
            logged_user = LoggedUser.objects.all().order_by('username')

            for i in logged_user:
                if i.username != username:
                    userlist.append(i.username)

            # smd format is used for display token
            smd = {
                'success': True,
                'message': "successfully logged",
                'token': token,
                'username': username,
                'userlist': userlist[1:],
            }
            messages.info(request, "logged in")
            return HttpResponse(json.dumps(smd))
        else:
            messages.info(request, "one of the above field is empty")
            # return redirect('/login')
            return Response("not registered yet")


@csrf_exempt
def forgot_password(request):
    """
    :param request: request is made for resetting password
    :return:  will return email where password reset link will be attached
    """
    global user, user_info
    if request.method == 'POST':
        email = request.POST["email"]

        # email validation is done here
        if email == "":
            messages.info(request, "please enter a vaild email address")
            return redirect('/login/forgotpassword')
        else:
            try:
                user = User.objects.get(email=email)
                user_info = Registration.objects.get(email=email)

                #  here user is not none then token is generated
                if user is not None:
                    username = user.username
                    password = user_info.password
                    data = {
                        'username': username,
                        'password': password
                    }
                    token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256").decode('utf-8')
                    # email is generated  where it is sent the email address entered in the form
                    mail_subject = "Activate your account by clicking below link"
                    mail_message = render_to_string('login/reset_password_token_link.html', {
                        'user': user.username,
                        'domain': get_current_site(request).domain,
                        'token': token
                    })
                    recipientemail = user.email
                    email = EmailMessage(mail_subject, mail_message, to=[recipientemail])
                    email.send()
                    # here email is sent to user
                    messages.info(request, "please check your mail for the resetting password ")
                else:
                    messages.info(request, 'not a registered email address')
                    return redirect('/login/forgotpassword')
            except Exception as e:
                messages.info(request, 'not a registered email address')
                return redirect('/login/forgotpassword')
            return redirect('/login/forgotpassword')
    else:
        return render(request, 'login/forgotpassword.html')


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
    except Exception as e:
        messages.info(request, 'activation link expired')
        return redirect('login/forgotpassword')


def resetpassword(request, user_reset):
    """
    :param user_reset:
    :param request:  user will request for resetting password
    :param userReset: username is fetched
    :return: will chnage the password
    """
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # password validation is done in this form
        if password1 == "" or password2 == "":
            messages.info(request, "please check the re entered password again")
            return redirect("/login/forgotpassword/resetpassword/" + str(user_reset))

        elif password2 != password1:
            messages.info(request, "please check the re entered password again")
            return redirect("/login/forgotpassword/resetpassword/" + str(user_reset))

        else:
            user = User.objects.get(username=user_reset)
            user.set_password(password1)
            # here we will save the user password in the database
            user.save()
            messages.info(request, "password reset done")
            return redirect("/login")
    else:
        return render(request, 'login/resetpassword.html')


def logout(request):
    """
    :param request: logout request is made
    :return: we will delete the token which was stored in redis
    """

    messages.info(request, "logged out")
    return render(request, 'login/logout.html')


def session(request):
    """
    :param request: request is made
    :return:  if token is deleted and user goes back then it will take to login page
    """
    return render(request, 'login/session.html')
