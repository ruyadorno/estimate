from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django_openid_auth.views import login_begin

from estimate import settings

@login_required
def home(request):
    return redirect('stories_index')

def login_view(request):
    return login_begin(request, template_name='login.html')

def logout_view(request):
    logout(request)
    return redirect(settings.LOGIN_URL)
