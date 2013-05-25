import logging
from decimal import Decimal
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

from django_openid_auth.views import login_begin

from estimate import settings
from estimate.forms import UserForm, GroupForm
from estimate.models import UserProxy, GroupProxy, GroupInfo


logger = logging.getLogger(__name__)

@login_required
def home(request):
    return redirect('stories_index')

def login_view(request):
    return login_begin(request, template_name='login.html')

def logout_view(request):
    logout(request)
    return redirect(settings.LOGIN_URL)

@login_required
def users(request):
    context = RequestContext(request, {
        'users':UserProxy.objects.all(),
    })
    return render_to_response('users.html', context)

@login_required
def user(request, user_id):
    if request.method == 'POST':
        if not request.user.has_perm('auth.change_userproxy'):
            return redirect('forbidden')
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
        })
    return form

def _render_user_page(request, user, form):
    context = RequestContext(request, {
        'edituser':user,
        'form':form,
        'show_hidden_fields':request.user.is_superuser,
        'is_editable':request.user.has_perm('auth.change_userproxy'),
        'is_me':request.user==user,
    })
    return render_to_response('user.html', context)

@login_required
@permission_required('auth.delete_userproxy', login_url='/notallowed/')
def remove_user(request):
    if request.method == 'POST':
        try:
            delete_id = request.POST['delete_id']
        except KeyError:
            return redirect('users')
        user = get_object_or_404(UserProxy, id=delete_id)
        user.delete()
        return redirect('users')
    else:
        raise Http404

@login_required
def groups(request):
    context = RequestContext(request, {
        'groups':GroupProxy.objects.all(),
        'is_superuser':request.user.is_superuser,
    })
    return render_to_response('groups.html', context)

@login_required
def group(request, group_id):
    if request.method == 'POST':
        if not request.user.has_perm('auth.change_groupproxy'):
            return redirect('forbidden')
        try:
            group = GroupProxy.objects.get(id=group_id)
        except GroupProxy.DoesNotExist:
            raise Http404
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            group = GroupProxy.objects.get(id=group_id)
            _save_group_modifier(request, group)
    else:
        group = get_object_or_404(GroupProxy, id=group_id)
        form = _get_group_form(group)
    return _render_group_page(request, group, form);

def _save_group_modifier(request, group):
    try:
        new_modifier = request.POST['modifier']
    except AttributeError:
        new_modifier = None
        logger.error('Saving a group without send a modifier value')
    if new_modifier != None:
        old_info = group.info
        groupinfo = GroupInfo()
        groupinfo.modifier=new_modifier
        groupinfo.group = group
        groupinfo.save()
        group.groupinfo_set.add(groupinfo)
        old_info.delete()

def _get_group_form(group):
    form = GroupForm({
        'id':group.id,
        'name':group.name,
        'permissions':[y.id for y in group.permissions.all()],
        }, instance=group)
    return form

def _render_group_page(request, group, form):
    context = RequestContext(request, {
        'group':group,
        'form':form,
        'modifier_value':group.modifier,
        'is_editable':request.user.has_perm('auth.change_groupproxy'),
    })
    return render_to_response('group.html', context)

@login_required
@permission_required('auth.add_groupproxy', login_url='/notallowed/')
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
@permission_required('auth.delete_groupproxy', login_url='/notallowed/')
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

def forbidden(request):
    return render_to_response('forbidden.html', RequestContext(request))
