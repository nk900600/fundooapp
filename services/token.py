import jwt
import requests
from fundoo import settings


def token_activation(username, password):

    data = {
        'username': username,
        'password': password
    }
    token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token


def token_validation(username, password):
    data = {
        'username': username,
        'password': password
    }
    r = requests.post(settings.AUTH_ENDPOINT, data=data)
    token = r.json()['access']
    return token