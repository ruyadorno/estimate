from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest
from django.contrib.auth.models import Permission

from estimate.models import UserProxy, GroupProxy
from estimate import receivers, settings


class SimpleTest(TestCase):

    fixtures = ['test_estimate.json', 'test_auth.json', 'test_stories.json']
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
        self._test_url_notloggedin('/')
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')
        self._logs_in_admin()
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
        self._logs_in_admin()
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')

    def test_users_page(self):
        "Test the /users/ page"
        self._test_url_notloggedin('/users/')
        # Test page loading
        user = self._logs_in_admin()
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        # Test success listing of users
        for user in UserProxy.objects.all():
            self.assertContains(response, user.first_name)

    def test_user(self):
        "Test the users page"
        user = self._logs_in_admin()
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
        self.assertNotContains(response, 'alert-error')
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

    def test_user_page(self):
        "Test the /me/ page"
        self._test_url_notloggedin('/me/')
        # Test user successfully see its page
        user = self._logs_in_admin()
        response = self.client.get('/me/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.id)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_remove_user(self):
        "Test removing an user"
        self._test_url_notloggedin('/remove_user/')
        # Remove user should be a post only page
        self._logs_in_admin()
        response_fail = self.client.get('/remove_user/')
        self.assertEqual(response_fail.status_code, 404)
        # Test an empty post
        user_count = UserProxy.objects.count()
        response_fail = self.client.post('/remove_user/')
        self.assertRedirects(response_fail, '/users/')
        self.assertEqual(user_count, UserProxy.objects.count())
        # Test a non existing id
        response_fail = self.client.post('/remove_user/', {'delete_id':'20'})
        self.assertEqual(response_fail.status_code, 404)
        # Add a new user so we can delete it after
        user = UserProxy.objects.create_user(
                'deletedmeuser', 'nop@nop.nop', '1234')
        user.first_name = 'Delete'
        user.last_name = 'Me'
        group = GroupProxy.objects.get(name='Standard')
        user.groups.add(group)
        user.save()
        user_count = UserProxy.objects.count()
        # Test user deletion
        id_deleted = user.id
        response = self.client.post('/remove_user/', {'delete_id':id_deleted})
        self.assertRedirects(response, '/users/')
        # Test database have actually been updated and check content
        self.assertNotEqual(user_count, UserProxy.objects.count())
        self.assertEqual(len(UserProxy.objects.filter(id=id_deleted)), 0)

    def test_groups_page(self):
        "Test the /groups/ page"
        self._test_url_notloggedin('/groups/')
        # Test page loading
        user = self._logs_in_admin()
        response = self.client.get('/groups/')
        self.assertEqual(response.status_code, 200)
        # Test success listing of groups
        groups = GroupProxy.objects.all()
        for group in groups:
            self.assertContains(response, group.name)
            for user in group.user_set.all():
                self.assertContains(response, user.first_name)

    def test_group_page(self):
        "Test the group detail page"
        self._logs_in_admin()
        # Fail when provide no group id
        response_fail = self.client.get('/group/')
        self.assertEqual(response_fail.status_code, 404)
        # Test user successfully see its page
        groups = GroupProxy.objects.all()
        for group in groups:
            response = self.client.get('/group/'+str(group.id))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, group.name)
            for perm in group.permissions.all():
                self.assertContains(response, perm.name)
            for user in group.user_set.all():
                self.assertContains(response, user.first_name)
            self.assertNotContains(response, 'alert-error')
        new_group_name = 'New group name'
        # Successfull update group data
        group = GroupProxy.objects.get(name='Standard')
        group_id = group.id
        response = self.client.post('/group/%s' % group.id,
                {
                    'name':new_group_name,
                }
        )
        group = GroupProxy.objects.get(id=group_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(group.name, new_group_name)

    def test_add_group(self):
        "Test the creation of a new group"
        self._test_url_notloggedin('/add_group/')
        # Get shouldn't work
        self._logs_in_admin()
        response_fail = self.client.get('/add_group/')
        self.assertEqual(response_fail.status_code, 404)
        # Create a new group
        group_count = GroupProxy.objects.count()
        name_added = 'Tchululu Group'
        response = self.client.post('/add_group/', { 'name':name_added, })
        self.assertRedirects(response, '/groups/')
        # Test database have actually been updated and check new content
        new_group_count = GroupProxy.objects.all().count()
        self.assertNotEqual(group_count, new_group_count)
        added_group = GroupProxy.objects.get(name=name_added)
        self.assertEqual(name_added, added_group.name)

    def test_remove_group(self):
        "Test removing a group"
        self._test_url_notloggedin('/remove_group/')
        # Remove group should be a post only page
        self._logs_in_admin()
        response_fail = self.client.get('/remove_group/')
        self.assertEqual(response_fail.status_code, 404)
        # Test an empty post
        group_count = GroupProxy.objects.count()
        response_fail = self.client.post('/remove_group/')
        self.assertRedirects(response_fail, '/groups/')
        self.assertEqual(group_count, GroupProxy.objects.count())
        # Test a non existing id
        response_fail = self.client.post('/remove_group/', {'delete_id':'20'})
        self.assertEqual(response_fail.status_code, 404)
        # Actually delete a post and test it
        id_deleted = GroupProxy.objects.all()[0].id
        response = self.client.post('/remove_group/', {'delete_id':id_deleted})
        self.assertRedirects(response, '/groups/')
        # Test database have actually been updated and check content
        self.assertNotEqual(group_count, GroupProxy.objects.count())

    def _test_url_notloggedin(self, url):
        response_fail = self.client.get(url)
        self.assertRedirects(response_fail, '/login/?next='+url)

    def _logs_in_admin(self):
        user = UserProxy.objects.create_user(
                self.USERNAME, self.USERMAIL, self.PASSWORD)
        user.first_name = self.USERNAME
        user.last_name = self.USERLASTNAME
        group = GroupProxy.objects.get(name='Standard')
        for perm in Permission.objects.all():
            group.permissions.add(perm)
        user.groups.add(group)
        user.save()
        self.client.login(username=self.USERNAME, password=self.PASSWORD)
        return user
