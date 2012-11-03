from django.test import TestCase
from django.test.client import Client

from stories.models import Project, Story


class SimpleTest(TestCase):

    urls = 'stories.urls'
    fixtures = ['test.json',]

    def setUp(self):
        "Set up test data"
        self.client = Client()
        self.projects = Project.objects.all()
        self.active_projects = Project.objects.filter(active=True)
        self.unactive_projects = Project.objects.filter(active=False)

    def test_fixtures(self):
        "Test fixtures are loaded and data is accessible"
        self.assertNotEqual(self.projects.count(), 0)

    def test_index(self):
        "Test the loading of index page"
        # Make request and assure status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Test for full content being provided
        self.assertEqual(
            len(response.context['projects']), self.active_projects.count()
        )
        # Test for provided data to view
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateNotUsed(response, 'project.html')
        for project in self.active_projects:
            self.assertContains(response, project.name, 1)
        for project in self.unactive_projects:
            self.assertNotContains(response, project.name)

    def test_add_project(self):
        "Test the add project page"
        # Add project should be a post only page
        response_fail = self.client.get('/add/')
        self.assertEqual(response_fail.status_code, 404)
        # Testing a post form
