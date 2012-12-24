from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render_to_response, redirect
from django_openid_auth.views import login_begin

from estimate import settings

@login_required
def home(request):
    return render_to_response('base.html', {})

def login_view(request):
    return login_begin(request, template_name='login.html')

def logout_view(request):
    logout(request)
    return redirect(settings.LOGIN_URL)
