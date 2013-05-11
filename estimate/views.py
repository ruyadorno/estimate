from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

from django_openid_auth.views import login_begin

from estimate import settings
from estimate.forms import UserForm, GroupForm
from estimate.models import UserProxy, GroupProxy


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
            user = UserProxy.objects.get(id=user_id)
    else:
        user = get_object_or_404(UserProxy, id=user_id)
        form = _get_user_form(user, request.user==user)
    return _render_user_page(request, user, form)

@login_required
def user_page(request):
    form = _get_user_form(request.user, True)
    return _render_user_page(request, request.user, form)

def _get_user_form(user, is_self=False):
    form = UserForm({
        'id':user.id,
        'first_name':user.first_name,
        'last_name':user.last_name,
        'email':user.email,
        'is_active':user.is_active,
        'is_superuser':user.is_superuser,
        'groups':[x.id for x in user.groups.all()],
        'is_me':is_self,
        })
    return form

def _render_user_page(request, user, form):
    context = RequestContext(request, {
        'user':user,
        'form':form,
        'show_hidden_fields':request.user.is_superuser,
    })
    return render_to_response('user.html', context)

@login_required
def groups(request):
    context = RequestContext(request, {
        'groups':GroupProxy.objects.all(),
        'is_superuser':request.user.is_superuser,
    })
    return render_to_response('groups.html', context)

@login_required
def group(request, group_id):
    pass

@login_required
@permission_required('auth.add_groupproxy', login_url='/login/')
def add_group(request):
    if request.method == 'POST':
        group = GroupProxy()
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('groups')
        else:
            return _add_group_error(request, form)
    else:
        raise Http404

@login_required
@permission_required('auth.delete_groupproxy', login_url='/login/')
def remove_group(request):
    if request.method == 'POST':
        try:
            delete_id = request.POST['delete_id']
        except KeyError:
            return redirect('groups')
        group = get_object_or_404(GroupProxy, id=delete_id)
        group.delete()
        return redirect('groups')
    else:
        raise Http404

def _add_group_error(request, form):
    context = RequestContext(request, {
        'groups':GroupProxy.objects.all(),
        'form':form,
    })
    return render_to_response('groups.html', context)
