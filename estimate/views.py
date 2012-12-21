from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response

@login_required(login_url='/openid/login/')
def home(request):
    return render_to_response('base.html', {})
