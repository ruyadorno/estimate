from django.test import TestCase
from django.test.client import Client

from stories.models import Project, Story


class SimpleTest(TestCase):

    fixtures = ['test.json',]

    def setUp(self):
        "Set up test data"
        self.client = Client()
        self.projects = Project.objects.all()
        self.active_projects = Project.objects.filter(active=True)

    def test_fixtures(self):
        "Test fixtures are loaded and data is accessible"
        self.assertNotEqual(self.projects.count(), 0)

    def test_index_page(self):
        "Test the loading of index page"
        response = self.client.get('/stories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context['projects']), self.active_projects.count()
        )
        for project in self.active_projects:
            self.assertContains(response, project.name, 1)
