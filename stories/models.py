from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField()

class Story(models.Model):
    name = models.CharField(max_length=100)
    time = models.IntegerField()
    accepted = models.BooleanField()
    project = models.ForeignKey(Project)
