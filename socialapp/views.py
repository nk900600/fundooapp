"""
 ******************************************************************************
 *  Purpose: Social login app is created where user can login using different
 *           service provider
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   19/11/2019
 ******************************************************************************
"""



import pdb

from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from authlib.integrations.requests_client import OAuth2Session
from rest_framework.generics import GenericAPIView

from fundoo.settings import SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, AUTH_GITHUB_URL, AUTH_GITHUB_TOKEN_URL, \
    BASE_URL, AUTH_GITHUB_USER_EMAIL_URL, AUTH_GITHUB_USER_URL, file_handler,logging
from lib.redis import red
from lib.token import token_validation
from socialapp.models import SocialLogin

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


class Github(GenericAPIView):
    """
        Summary:
        --------
            Github class is a logic written where redirected url is github login page containing state and scope in header.

        Methods:
        --------
            get: User will get a github login url page where he will enter git hub credentials

    """

    def get(self, request):
        # pdb.set_trace()
        resp = {'success': False, 'message': "something went wrong", 'data': []}
        try:
            auth_url = AUTH_GITHUB_URL
            scope = 'user:email'
            client = OAuth2Session(SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, scope=scope)
            url, state = client.create_authorization_url(auth_url)
            logger.info("redirected user to github login page",)
            return redirect(url)
        except Exception as e:
            logger.error("got %s error while redirecting the user to github login page ", str(e))
            return HttpResponse(resp,status=404)


class Oauth(GenericAPIView):
    """
      Summary:
      --------
          After user getting redirected to this class we will able to fetch token which will be created once we
          provide client-key and client-secret. Once we fetch the token then we have to hit github user page and then
          we will able to fetch user details excluding password

      Methods:
      --------
          get: User details will be fetched after checking the access token

    """
    def get(self, request):

        resp = {'success': False, 'message': "something went wrong", 'data': []}
        try:
            # pdb.set_trace()
            token_url = AUTH_GITHUB_TOKEN_URL    # github token url.
            scope = 'user:email'
            client = OAuth2Session(SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, scope=scope)

            # here token is fetched after passing below params.
            token = client.fetch_token(token_url, client_id=SOCIAL_AUTH_GITHUB_KEY, client_secret=SOCIAL_AUTH_GITHUB_SECRET
                                       ,authorization_response=BASE_URL+request.get_full_path())
            client = OAuth2Session(SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, token=token,scope=scope)
            account_url_email = AUTH_GITHUB_USER_EMAIL_URL
            account_url= AUTH_GITHUB_USER_URL

            # we will get response after hiting github url with proper access_token,code and state.
            response = client.get(account_url)
            response_email = client.get(account_url_email)

            # response will contain all the details of the user which he authorised.
            user_details=response.json()
            email_id=response_email.json()[0]["email"]
            username= response.json()["login"]
            first_name = user_details["name"].split(" ")[0]
            last_name = user_details["name"].split(" ")[1]

            # first we will check if we have registered this user if yes then we will generate JWT token and redirect.
            if SocialLogin.objects.filter(unique_id=response.json()["id"]).exists():
                user = auth.authenticate(username=username, password=response.json()["id"])
                token = token_validation(user.username, response.json()["id"])
                auth.login(request, user)
                red.set(user.username, token)
                logger.info("%s logged in using social auth ",user.username)
                # return redirect("/api/notes/")
            else:

                # if we have not registered this user then we save user details in SocialLogin page.
                SocialLogin.objects.create(unique_id=response.json()["id"], provider="github", full_name=user_details["name"],
                                           username=username, EXTRA_PARAMS=response.json())

                # if registered user has same user name matching in db then we will use his unique_id as username and
                # save the user.
                if User.objects.filter(username=username).exists():

                    user = User.objects.create_user(username=response.json()["id"], first_name=first_name, last_name=last_name,
                                                    email=email_id, password=response.json()["id"])
                    user.save()
                    token = token_validation(username, response.json()["id"])
                    red.set(user.username, token)
                    logger.info("%s logged in as well as user got registered but username already exixt so his id "
                                "is as his username ", user.username)
                else:

                    # here we will save the user details and generate jwt token and then redirect to dashboard.
                    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                    email=email_id,password=response.json()["id"])
                    user.save()
                    token = token_validation(username, response.json()["id"])
                    red.set(user.username, token)
                    logger.info("%s logged in as well as user got registered ", user.username)

            # once user is registered or logged in user is redirected to dashboard
            return redirect("/api/notes/")
        except Exception as e:
            logger.error("error: %s while registering user or while logging in ",str(e))
            return HttpResponse(resp ,status=404)
