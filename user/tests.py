from django.test import TestCase
import pytest
import requests
import unittest

# Create your tests here.

base_url = 'http://127.0.0.1:8000'
registration = {
    "name": "nikhil",
    'username': 'nk90600',
    'email': 'niksroad2success@gamil.com',
    'password1': "pankaj",
    'password2': "pankaj"
}

login = {
    'username': 'admin',
    'password': "admin",
}


class TestRegistration(unittest.TestCase):

    def test_registration(self):
        url = base_url + '/registration'
        data = registration
        response = requests.post(url=url, data=data)
        assert response.status_code == 200

    def test_login(self):
        url = base_url + '/login'
        data = login
        response = requests.post(url=url, data=data)
        assert response.status_code == 200


if __name__ == '__main__':
    TestRegistration()
    # test_login()
