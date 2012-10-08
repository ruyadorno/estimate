from django.db import models


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


class Story(models.Model):
    name = models.CharField(max_length=100)
    time = models.IntegerField()
    accepted = models.BooleanField()
    project = models.ForeignKey(Project)
