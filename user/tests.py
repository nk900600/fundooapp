"""
this file is created for test cases, test case for registrations and login apis are ran 
"""
import requests
import unittest

# Create your tests here.

BASE_URL = 'http://127.0.0.1:8000'
RESGISTRATION = {
    "name": "nikhil",
    'username': 'nk90600',
    'email': 'niksroad2success@gamil.com',
    'password1': "pankaj",
    'password2': "pankaj"
}

LOGIN = {
    'username': 'admin',
    'password': "admin",
}


class TestRegistration(unittest.TestCase):
    """
    test case is created and test with predefined values
    """
    def test_registration(self):
        """
        test case is created for registrations and test with predefined values
        """
        url = BASE_URL + '/registration'
        data = RESGISTRATION
        response = requests.post(url=url, data=data)
        assert response.status_code == 200

    def test_login(self):
        """
        test case is created for login and test with predefined values
        """
        url = BASE_URL + '/login'
        data = LOGIN
        response = requests.post(url=url, data=data)
        assert response.status_code == 200


if __name__ == '__main__':
    TestRegistration()
    # test_login()
