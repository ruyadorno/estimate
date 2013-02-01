from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest

from estimate.models import UserProxy, GroupProxy
from estimate import receivers, settings


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
        "Test logout"
        self._logs_in()
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')

    def test_handle_openid_complete(self):
        group = GroupProxy.objects.get(name='Standard')
        self.assertEqual(group.user_set.count(), 0)
        request = HttpRequest()
        request.user = self._logs_in()
        receivers.handle_openid_login(request, {})
        if settings.AUTO_CREATE_SUPERUSER:
            self.assertEqual(group.user_set.all()[0].id, request.user.id)

    def test_user(self):
        "Test the users page"
        user = self._logs_in()
        # Fail when provide no user id
        response_fail = self.client.get('/user/')
        self.assertEqual(response_fail.status_code, 404)
        # Get user page successfully
        response = self.client.get('/user/%s' % user.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.id)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
        new_first_name = 'Lorem'
        new_last_name = 'Ipsum'
        new_email = 'teste@teste.com'
        # Successfull update user data
        response = self.client.post('/user/%s' % user.id,
                {
                    'first_name':new_first_name,
                    'last_name':new_last_name,
                    'email':new_email,
                }
        )
        self.assertEqual(response.status_code, 200)
        user = UserProxy.objects.get(id=user.id)
        self.assertEqual(user.first_name, new_first_name)
        self.assertEqual(user.last_name, new_last_name)
        self.assertEqual(user.email, new_email)
        self.assertContains(response, user.id)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def _logs_in(self):
        user = UserProxy.objects.create_user(
                self.USERNAME, self.USERMAIL, self.PASSWORD)
        user.last_name = self.USERLASTNAME
        user.save()
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        return user
