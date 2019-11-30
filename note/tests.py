import json
import pdb

import pytest
import requests
from django.contrib.auth.models import User

from fundoo.settings import BASE_URL, TEST_TOKEN
from django.test import Client, override_settings

from lib.token import token_validation

from django.test import TestCase
from django.urls import reverse


from note.models import Notes, Label
import unittest


class ModelsTest(TestCase):
    fixtures = ['test_fundoo_db']

    def test_note_string_representation1(self):
        entry = Notes(note="My entry title")
        self.assertEqual(str(entry), entry.note)

    def test_login(self):
        global header
        # pdb.set_trace()
        login_url = BASE_URL + reverse('login')
        resp = self.client.post(login_url, {'username': 'admin', 'password': 'admin'}, )
        self.assertEqual(resp.status_code, 201)
        note_url = BASE_URL + reverse('note_update', args=[1])
        header = {'HTTP_AUTHORIZATION': "Bearer "+json.loads(resp.content)["data"][0]}
        resp = self.client.get(note_url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 200)

    def test_note_get2(self):
        url = BASE_URL + reverse('note_update', args=["fbv"])
        resp = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 404)

    def test_note_string_representation2(self):
        entry = Notes(title="My entry title")
        self.assertEqual(str(entry), "")
    #
    # def test_note_equal1(self):
    #     note1 = Notes(note="My entry note")
    #     note2 = Notes(note="My entry note")
    #     self.assertFalse(note1 == note2, True)
    #
    # def test_note_equal2(self):
    #     note1 = Notes(note="My first note")
    #     note2 = Notes(note="My second note ")
    #     self.assertFalse(note1 == note2, True)

    def test_note_isinstance1(self):
        user1 = User(username="nikhil")
        note2 = Notes(note="My second note ")
        self.assertEqual(user1 == note2, False)

    def test_note_isinstance2(self):

        user1 = User(username="nikhil")
        note2 = Notes(note="My second note ")
        self.assertFalse(user1 == note2, "hello")

    def test_note_verbose_name_plural1(self):
        self.assertEqual(str(Notes._meta.verbose_name_plural), "Notes")

    def test_note_verbose_name_plural2(self):
        self.assertNotEqual(str(Notes._meta.verbose_name_plural), "testing")

    def test_note_verbose_name1(self):
        self.assertEqual(str(Notes._meta.verbose_name), "Note")

    def test_note_verbose_name2(self):
        self.assertNotEqual(str(Notes._meta.verbose_name), "testing")

    ############################################################################

    def test_label_string_representation1(self):
        entry = Label(name="My name")
        self.assertEqual(str(entry), entry.name)

    def test_label_string_representation2(self):
        entry = Label(name="My name")
        self.assertNotEqual(str(entry), "")

    # def test_label_equal1(self):
    #     Label1 = Label(name="My entry label")
    #     Label2 = Label(name="My entry label")
    #     self.assertTrue(Label1 == Label2, True)

    def test_label_equal2(self):
        Label1 = Label(name="My first label")
        Label2 = Label(name="My second label ")
        self.assertFalse(Label1 == Label2, True)

    def test_label_isinstance1(self):
        user1 = User(username="nikhil")
        Label2 = Label(name="My second label ")
        self.assertEqual(user1 == Label2, False)

    def test_label_isinstance2(self):
        user1 = User(username="nikhil")
        Label2 = Label(name="My second label ")
        self.assertFalse(user1 == Label2, "hello")

    def test_label_verbose_name_plural1(self):
        self.assertEqual(str(Label._meta.verbose_name_plural), "labels")

    def test_label_verbose_name_plural2(self):
        self.assertNotEqual(str(Label._meta.verbose_name_plural), "testing")

    def test_label_verbose_name1(self):
        self.assertEqual(str(Label._meta.verbose_name), "label")

    def test_label_verbose_name2(self):
        self.assertNotEqual(str(Label._meta.verbose_name), "testing")


class NotesTest(TestCase):
    fixtures = ['test_fundoo_db']

    def test_note_getall1(self):
        url = BASE_URL + reverse('notes')
        resp = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

    def test_note_get1(self):
        url = BASE_URL + reverse('note_update', args=[1])
        resp = self.client.get(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 200)

    def test_note_get2(self):
        url = BASE_URL + reverse('note_update', args=["fbv"])
        resp = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 404)

    def test_note_get3(self):
        url = BASE_URL + reverse('note_update', args=[1000])
        resp = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

    def test_note_post1(self):
        url = BASE_URL + reverse('notes')
        data = {"title": "hii", "note": "heelo", "label": ["hheelo"]}
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_note_post2(self):
        url = BASE_URL + reverse('notes')
        data = {"title": "hii", "note": "heelo", "label": ["japan"]}
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 201)

    def test_note_post23(self):
        url = BASE_URL + reverse('notes')
        data = {"title": "hii", "note": "heelo", "is_archive": 'true'}
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 201)

    def test_note_post3(self):
        url = BASE_URL + reverse('notes')
        data = {"title": "hii", "note": "heelo", "collaborators": ["nk90600@gmail.com"]}
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 201)

    def test_note_post5(self):
        url = BASE_URL + reverse('notes')
        data = {"title": "hii", "efdef": "heelo", "collaborators": ["nk90600@gmail.com"]}
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 201)

    def test_note_post4(self):
        url = BASE_URL + reverse('notes')
        data = {"title": "hii", "note": "heelo", "url": "google.com"}
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_note_put1(self):
        url = BASE_URL + reverse('note_update', args=[1])
        data = {"title": "hii", "note": "heelo", "url": "google.com"}
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_note_put11(self):
        url = BASE_URL + reverse('note_update', args=[1])
        data = {"title": "hii", "note": "heelo", "is_archive": "true"}
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

    def test_note_put10(self):
        url = BASE_URL + reverse('note_update', args=[1])
        data = {"title": "hii", "note": "heelo", "is_trashed": "true"}
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

    def test_note_put6(self):
        url = BASE_URL + reverse('note_update', args=[1])
        data = {"title": "hii", "wfwfwfwf": "heelo", "url": "google.com"}
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_note_put5(self):
        url = BASE_URL + reverse('note_update', args=[1])
        data = {"title": "hii", "note": "heelo","collaborators": ["nk90600@gmail.com"]}
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

    def test_note_put2(self):
        url = BASE_URL + reverse('note_update', args=[1])
        data = {"title": "hii", "note": "heelo", }
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

    def test_note_put3(self):
        url = BASE_URL + reverse('note_update', args=[1])
        data = {"title": "hii", "note": "heelo", "label": ["google.com"]}
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_note_delete1(self):
        url = BASE_URL + reverse('note_update', args=[500])
        resp = self.client.delete(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 404)

    def test_note_delete2(self):
        url = BASE_URL + reverse('note_update', args=[1])
        resp = self.client.delete(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 201)

    def test_note_delete3(self):
        url = BASE_URL + reverse('note_update', args=[1])
        resp = self.client.delete(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 201)

    def test_label_get1(self):
        url = BASE_URL + reverse('label_get')
        resp = self.client.get(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 200)

    # def test_label_get2(self):
    #     url = BASE_URL + reverse('label_get')
    #     resp = self.client.get(url, content_type='application/json', **header)
    #     # print(resp.META)
    #     self.assertEqual(resp.status_code, 200)
    #
    # def test_label_get3(self):
    #     url = BASE_URL + reverse('label_get')
    #     resp = self.client.get(url, content_type='application/json', **header)
    #     # print(resp.META)
    #     self.assertEqual(resp.status_code, 200)

    def test_label_post1(self):
        url = BASE_URL + reverse('label_get')
        data = {"name": "", }
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_label_post2(self):
        url = BASE_URL + reverse('label_get')
        data = {"name": "japan", }
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_label_post4(self):
        url = BASE_URL + reverse('label_get')
        data = {"name": "hiiii", }
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 201)

    def test_label_post3(self):
        url = BASE_URL + reverse('label_get')
        data = {"name": "e", }
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_label_put1(self):
        url = BASE_URL + reverse('label_update', args=[8])
        data = {"name": "japan", }
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

    def test_label_put2(self):
        url = BASE_URL + reverse('label_update', args=[80])
        data = {"name": "japan", }
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 404)

    def test_label_put3(self):
        url = BASE_URL + reverse('label_update', args=["gfgfbh"])
        data = {"name": "japan", }
        resp = self.client.put(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 404)

    def test_label_delete1(self):
        url = BASE_URL + reverse('label_update', args=[80])
        resp = self.client.delete(url, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 404)

    def test_label_delete2(self):
        url = BASE_URL + reverse('label_update', args=["gnf"])
        resp = self.client.delete(url, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 404)

    def test_label_delete3(self):
        url = BASE_URL + reverse('label_update', args=[9])
        resp = self.client.delete(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 404)

    def test_reminders(self):
        url = BASE_URL + reverse('reminder')
        resp = self.client.get(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 200)

    def test_archive(self):
        url = BASE_URL + reverse('archive')
        resp = self.client.get(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 200)

    def test_trashed(self):
        url = BASE_URL + reverse('trash')
        resp = self.client.get(url, content_type='application/json', **header)
        # print(resp.META)
        self.assertEqual(resp.status_code, 200)

    def test_note_share1(self):
        url = BASE_URL + reverse('note_share')
        data = {"title": "japan", "note": "hi"}
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 302)

    def test_note_share2(self):
        url = BASE_URL + reverse('note_share')
        data = {"note": "japan", }
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_celery(self):
        url = BASE_URL + reverse('celery')
        resp = self.client.get(url, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

    def test_search1(self):
        url = BASE_URL + reverse('search')
        data = {"title": "japan", }
        resp = self.client.post(url, data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 400)

    def test_search2(self):
        url = BASE_URL + reverse('search')
        data = {"note": "japan", }
        resp = self.client.post(url,data, content_type='application/json', **header)
        self.assertEqual(resp.status_code, 200)

