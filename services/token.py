"""
 ******************************************************************************
 *  Purpose: will generate token
 *
 *  @author  Nikhil Kumar
 *  @version 3.7
 *  @since   30/09/2019
 ******************************************************************************
"""

import jwt
import requests
from fundoo.settings import SECRET_KEY, AUTH_ENDPOINT


def token_activation(username, password):
    """
    :param username: takes user name as parameter
    :param password: takes password
    :return: will return token
    """

    data = {
        'username': username,
        'password': password
    }
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token


def token_validation(username, password):
    """
    :param username: takes user name as parameter
    :param password: takes password
    :return: will return token
    """
    data = {
        'username': username,
        'password': password
    }
    tokson = requests.post(AUTH_ENDPOINT, data=data)
    token = tokson.json()['access']
    return token
