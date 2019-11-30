"""
this file is created for test cases, test case for registrations and login apis are ran 
"""

import json
import requests
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from fundoo.settings import BASE_URL
#
# with open("test.json") as f:
#     data = json.load(f)


#
# class TestRegistration:
#     """
#     test case is created and test with predefined values
#     """
#     def test_registration1(self):
#         """
#         test case is created for registrations and test with predefined values
#         """
#         url = BASE_URL + '/registration/'
#         file = data[0]['test1']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 201
#
#     def test_registration2(self):
#         """
#         test case is created for registrations and test with predefined values
#         """
#         url = BASE_URL + '/registration/'
#         file = data[0]['test2']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 400
#
#
#     def test_registration3(self):
#         """
#         test case is created for registrations and test with predefined values
#         """
#         url = BASE_URL + '/registration/'
#         file = data[0]['test3']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 201
#
#     def test_login1(self):
#         """
#         test case is created for login and test with predefined values
#         """
#         url = BASE_URL + '/login/'
#         file = data[0]['test4']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 201
#
#     def test_login2(self):
#         """
#         test case is created for login and test with predefined values
#         """
#         url = BASE_URL + '/login/'
#         file = data[0]['test5']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 400
#
#     def test_login3(self):
#         """
#         test case is created for login and test with predefined values
#         """
#         url = BASE_URL + '/login/'
#         file = data[0]['test6']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 400
#
#     def test_reset_password_1(self):
#         """
#         test case is created for login and test with predefined values
#         """
#         url = BASE_URL + '/resetpassword/'+data[0]['test12']['user_reset']
#         file = data[0]['test12']['password']
#         response = requests.post(url=url, data=file)
#         assert response.status_code == 404
#
#
# if __name__ == '__main__':
#     TestRegistration()
#     # test_login()
from user.models import Registration


class ModelTest(TestCase):
    fixtures = ['test_fundoo_db']


    def test_label_string_representation1(self):
        entry = Registration(name="My name")
        self.assertEqual(str(entry), entry.name)

    def test_label_string_representation2(self):
        entry = Registration(name="My name")
        self.assertNotEqual(str(entry), "")

    def test_label_equal1(self):
        user1 = Registration(name="nikhil")
        user2 = Registration(name="nikhil")
        self.assertTrue(user1 == user2, True)

    def test_label_equal2(self):
        user1 = Registration(name="nikhil")
        user2 = Registration(name="pankaj ")
        self.assertFalse(user1 == user2, True)

    def test_label_isinstance1(self):
        user1 = User(username="nikhil")
        user2 = Registration(name="nikhil ")
        self.assertEqual(user1 == user2, False)

    def test_label_isinstance2(self):
        user1 = User(username="nikhil")
        user2 = Registration(name="nikhil ")
        self.assertFalse(user1 == user2, "hello")

    def test_label_verbose_name_plural1(self):
        self.assertEqual(str(Registration._meta.verbose_name_plural), "user details")

    def test_label_verbose_name_plural2(self):
        self.assertNotEqual(str(Registration._meta.verbose_name_plural), "testing")

    def test_label_verbose_name1(self):
        self.assertEqual(str(Registration._meta.verbose_name), "user detail")

    def test_label_verbose_name2(self):
        self.assertNotEqual(str(Registration._meta.verbose_name), "testing")


class LoginsTest(TestCase):
    fixtures = ['test_fundoo_db']

    def test_registration1(self):
        url = BASE_URL + reverse('registration')
        resp = self.client.post(url, {'username': '', 'password': 'admin', 'email': 'nk90600@gmail.com'})
        # print(resp.META)
        self.assertEqual(resp.status_code, 400)

    def test_registration2(self):
        url = BASE_URL + reverse('registration')
        resp = self.client.post(url, {'username': 'admin', 'password': 'admin', 'email': 'nk90600@gmail.com'})
        # print(resp.META)
        self.assertEqual(resp.status_code, 400)

    def test_registration3(self):
        url = BASE_URL + reverse('registration')
        resp = self.client.post(url, {'username': 'hello', 'password': 'world', 'email': 'now@gmail.com'})
        # print(resp.META)
        self.assertEqual(resp.status_code, 201)

    def test_registration4(self):
        url = BASE_URL + reverse('registration')
        resp = self.client.post(url, {'username': 'hello', 'password': 'world', 'email': 'nowddcom'})
        # print(resp.META)
        self.assertEqual(resp.status_code, 400)

    def test_login1(self):
        url = BASE_URL + reverse('login')
        resp = self.client.post(url, {'username': 'admin', 'password': 'admin'}, )
        self.assertEqual(resp.status_code, 201)


    def test_login2(self):
        url = BASE_URL + reverse('login')
        resp = self.client.post(url, {'username': 'rfg', 'password': 'fg'}, )
        self.assertEqual(resp.status_code, 400)

    def test_login3(self):
        url = BASE_URL + reverse('login')
        resp = self.client.post(url, {'username': '', 'password': 'admin'}, )
        self.assertEqual(resp.status_code, 400)

    def test_login4(self):
        url = BASE_URL + reverse('login')
        resp = self.client.post(url, {'hrhrh': 'rhr', 'password': 'admin'}, )
        self.assertEqual(resp.status_code, 400)

    def test_forgotpassword1(self):
        url = BASE_URL + reverse('forgotPassword')
        resp = self.client.post(url, {'email': ''}, )
        self.assertEqual(resp.status_code, 400)

    def test_forgotpassword2(self):
        url = BASE_URL + reverse('forgotPassword')
        resp = self.client.post(url, {'email': 'nk90600@gmail.com'}, )
        self.assertEqual(resp.status_code, 201)

    def test_forgotpassword3(self):
        url = BASE_URL + reverse('forgotPassword')
        resp = self.client.post(url, {'email': 'nikhil'}, )
        self.assertEqual(resp.status_code, 400)

    def test_resetpassword1(self):
        url = BASE_URL + reverse('resetpassword', args=["admin"])
        resp = self.client.post(url, {'password': 'admin'}, )
        self.assertEqual(resp.status_code, 201)

    def test_resetpassword2(self):
        url = BASE_URL + reverse('resetpassword', args=["hghgh"])
        resp = self.client.post(url, {'password': 'bgf'}, )
        self.assertEqual(resp.status_code, 400)

    def test_logout1(self):
        url = BASE_URL + reverse('logout')
        resp = self.client.get(url, )
        self.assertEqual(resp.status_code, 200)

    def test_pass1(self):
        url = BASE_URL + reverse('reset_password', args=['pWVEbCXZKisLXDSHZgdAte'])
        resp = self.client.get(url, )
        self.assertEqual(resp.status_code, 302)

    def test_pass2(self):
        url = BASE_URL + reverse('reset_password', args=['dvdvdvdv'])
        resp = self.client.get(url, )
        self.assertEqual(resp.status_code, 302)

    def test_pass3(self):
        url = BASE_URL + reverse('reset_password', args=['pWVEbCXZKivdvdvdvdsLXDSHZgdAte'])
        resp = self.client.get(url, )
        self.assertEqual(resp.status_code, 302)

    # def test_activate1(self):
    #     url = BASE_URL + reverse('activate', args=['tghjgn'])
    #     resp = self.client.get(url, )
    #     self.assertEqual(resp.status_code, 302)

    def test_activate2(self):
        url = BASE_URL + reverse('activate', args=['pWVEbCXZKisLXDSHZgdAte'])
        resp = self.client.get(url, )
        self.assertEqual(resp.status_code, 302)
