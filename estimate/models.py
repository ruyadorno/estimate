from django.db import models
from django.contrib.auth.models import Group


class GroupInfo(models.Model):
    modifier = models.DecimalField(max_digits=5, decimal_places=2)
    group = models.ForeignKey(Group)
