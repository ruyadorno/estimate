import logging
from django.db import models

from estimate.models import UserProxy, GroupProxy


logger = logging.getLogger(__name__)

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField()

    def __unicode__(self):
        return self.name


class Story(models.Model):
    name = models.CharField(max_length=100)
    time = models.DecimalField(max_digits=5, decimal_places=2)
    accepted = models.BooleanField()
    project = models.ForeignKey(Project)
    user = models.ForeignKey(UserProxy)

    def _get_group(self):
        try:
            group = GroupProxy.objects.get(self.user.group.id)
        except Exception:
            logger.warning(
                'Could not access the group of a given user'
            )
            try:
                group = GroupProxy.objects.get(name='Standard')
            except GroupProxy.DoesNotExist:
                group = GroupProxy()
        return group

    def _get_modifier(self):
        group = self.group
        try:
            modifier = group.modifier
        except Exception:
            logger.warning(
                'Could not access the info of a given group'
            )
            modifier = 1
        return modifier

    def _total_time(self):
        return self.time*self.modifier

    group = property(_get_group)
    modifier = property(_get_modifier)
    total_time = property(_total_time)

    def __unicode__(self):
        return self.name
