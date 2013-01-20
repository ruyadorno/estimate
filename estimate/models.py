import logging
from django.db import models
from django.contrib.auth.models import Group, User


logger = logging.getLogger(__name__)

class GroupInfo(models.Model):
    modifier = models.DecimalField(max_digits=5, decimal_places=2)
    group = models.ForeignKey(Group)


class UserProxy(User):

    def _group(self):
        if self.groups.count()<1:
            group = self._get_unassigned_group()
        elif self.groups.count()>1:
            logger.warning('User has more than one group assigned: '+self.id)
        group = GroupProxy.objects.get(id=self.groups.all()[0].id)
        return group

    def _get_unassigned_group(self):
        try:
            group = Group.objects.get(id=1)
        except Group.DoesNotExist:
            try:
                group = Group.objects.all()[0]
            except Exception:
                logger.error('No groups found for the given user: '+self.id)
        group.user_set.add(self)
        return group

    def _modifier(self):
        return self.group.modifier

    group = property(_group)
    modifier = property(_modifier)

    class Meta:
        proxy=True


class GroupProxy(Group):

    def _modifier(self):
        return self.info.modifier

    def _get_unassigned_groupinfo(self):
        if GroupInfo.objects.count()<1:
            logger.warning('No GroupInfo object was found on db')
            groupInfo = GroupInfo.objects.create(modifier=1)
            groupInfo.save()
        elif GroupInfo.objects.filter(modifier=1).count()>1:
            groupInfo = GroupInfo.objects.filter(modifier=1)[0]
        else:
            groupInfo = GroupInfo.objects.all()[0]
        self.groupinfo_set.add( groupInfo )
        return groupInfo

    def _groupinfo(self):
        if self.groupinfo_set.count()<1:
            groupInfo = self._get_unassigned_groupinfo()
        elif self.groupinfo_set.count()>1:
            logger.warning(
                    'Group has more than one groupinfo assigned: '+self.id)
        groupInfo = self.groupinfo_set.all()[0]
        return groupInfo

    info = property(_groupinfo)
    modifier = property(_modifier)

    class Meta:
        proxy=True
