from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField()

    def _get_total_time(self):
        try:
            stories = Story.objects.filter(project_id=self.id)
        except Exception:
            return 0
        times = [story.time for story in stories]
        return sum(times)

    total_time = property(_get_total_time)

    def __unicode__(self):
        return self.name


class Story(models.Model):
    name = models.CharField(max_length=100)
    time = models.DecimalField(max_digits=5, decimal_places=2)
    accepted = models.BooleanField()
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name
