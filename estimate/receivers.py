from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django_openid_auth.signals import openid_login_complete

from estimate import settings

@receiver(openid_login_complete)
def handle_openid_login(request, openid_response, **kwargs):
    if settings.AUTO_CREATE_SUPERUSER and _is_first_created_user():
        _create_superuser(request)

def _is_first_created_user():
    return User.objects.count() < 3

def _create_superuser(request):
    user = request.user
    user.is_staff = True
    user.is_superuser = True
    _add_to_standard_group(user)
    user.save()

def _add_to_standard_group(user):
    try:
        group = Group.objects.get(id=1)
    except Group.DoesNotExist:
        if Group.objects.count()>0:
            group = Group.objects.all()[0]
        else:
            group = None
    if group != None:
        group.user_set.add(user)
