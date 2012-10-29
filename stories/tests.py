from django.utils import unittest
from django.test import TestCase

from stories.models import Project, Story


class SimpleTest(TestCase):
    fixtures = ['test.json',]
    def test_basic_addition(self):
        print Project.objects.all()
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
