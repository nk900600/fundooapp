"""
this file is created for test cases, test case for registrations and login apis are ran 
"""

import json
import requests
from fundoo.settings import BASE_URL

with open("test.json") as f:
    data = json.load(f)


class TestRegistration:
    """
    test case is created and test with predefined values
    """
    def test_registration1(self):
        """
        test case is created for registrations and test with predefined values
        """
        url = BASE_URL + '/registration/'
        file = data[0]['test1']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200

    def test_registration2(self):
        """
        test case is created for registrations and test with predefined values
        """
        url = BASE_URL + '/registration/'
        file = data[0]['test2']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200


    def test_registration3(self):
        """
        test case is created for registrations and test with predefined values
        """
        url = BASE_URL + '/registration/'
        file = data[0]['test3']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200

    def test_login1(self):
        """
        test case is created for login and test with predefined values
        """
        url = BASE_URL + '/login/'
        file = data[0]['test4']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200

    def test_login2(self):
        """
        test case is created for login and test with predefined values
        """
        url = BASE_URL + '/login/'
        file = data[0]['test5']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200

    def test_login3(self):
        """
        test case is created for login and test with predefined values
        """
        url = BASE_URL + '/login/'
        file = data[0]['test6']
        response = requests.post(url=url, data=file)
        assert response.status_code == 200


if __name__ == '__main__':
    TestRegistration()
    # test_login()
