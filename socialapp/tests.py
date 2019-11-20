from django.test import TestCase

# Create your tests here.
from rest_framework.reverse import reverse

from fundoo.settings import BASE_URL
from note.models import Notes
from socialapp.models import SocialLogin


class ModelsTest(TestCase):
    fixtures = ['test_fundoo_db']

    def test_social_string_representation1(self):
        social = SocialLogin(provider="github",username="nikhil")
        self.assertEqual(str(social), "github nikhil")

    def test_social_string_representation2(self):
        social = SocialLogin(username="nikhil")
        self.assertEqual(str(social), " nikhil")

    def test_social_verbose_name_plural1(self):
        self.assertEqual(str(SocialLogin._meta.verbose_name_plural), "social login users")

    def test_social_verbose_name_plural2(self):
        self.assertEqual(str(SocialLogin._meta.verbose_name), "social login user")

    def test_social_verbose_name_plural3(self):
        self.assertNotEqual(str(SocialLogin._meta.verbose_name_plural), "social login user")

    def test_social_verbose_name_plural4(self):
        self.assertNotEqual(str(SocialLogin._meta.verbose_name), "social login users")

    def test_social_equal1(self):
        social1 = SocialLogin(username="My entry note")
        social2 = SocialLogin(username="My entry note")
        self.assertTrue(social1 == social2, True)

    def test_social_equal2(self):
        social1 = SocialLogin(username="My first note")
        social2 = SocialLogin(username="My second note ")
        self.assertFalse(social1 == social2, True)


class SocialTest(TestCase):
    fixtures = ['test_fundoo_db']

    def test_social_getall1(self):
        url = BASE_URL + reverse('github')
        resp = self.client.get(url, content_type='application/json',)
        self.assertEqual(resp.status_code, 302)

    def test_social_getall2(self):
        url = BASE_URL + reverse('oauth')
        resp = self.client.get(url, content_type='application/json', )
        self.assertEqual(resp.status_code, 404)
