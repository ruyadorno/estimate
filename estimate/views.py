from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

from django_openid_auth.views import login_begin

from estimate import settings
from estimate.forms import UserForm
from estimate.models import UserProxy

@login_required
def home(request):
    return redirect('stories_index')

def login_view(request):
    return login_begin(request, template_name='login.html')

def logout_view(request):
    logout(request)
    return redirect(settings.LOGIN_URL)

@login_required
def user(request, user_id):
    if request.method == 'POST':
        try:
            user = UserProxy.objects.get(id=user_id)
        except UserProxy.DoesNotExist:
            raise Http404
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        user = get_object_or_404(UserProxy, id=user_id)
        form = UserForm({
            'id':user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            })
    context = RequestContext(request, {
        'user':user,
        'form':form
    })
    return render_to_response('user.html', context)

@login_required
def user_page(request):
    pass
