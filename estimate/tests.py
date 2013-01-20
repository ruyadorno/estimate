from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User


class SimpleTest(TestCase):

    testuser = None

    USERNAME = 'testusername'
    USERLASTNAME = 'Lastname'
    USERMAIL = 'testusermail@test.com'
    PASSWORD = 'testpassword'

    def setUp(self):
        "Set up test data"
        self.client = Client()

    def test_index(self):
        "Test the loading of index page"
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')
        self._logs_in()
        response = self.client.get('/')
        self.assertRedirects(response, '/stories/')

    def test_login(self):
        "Test the loading of login page"
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'openid')

    def test_logout(self):
        self._logs_in()
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')

    def _logs_in(self):
        user = User.objects.create_user(self.USERNAME, self.USERMAIL, self.PASSWORD)
        user.last_name = self.USERLASTNAME
        user.save()
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
