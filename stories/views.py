from django.http import Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext

from estimate.models import UserProxy
from stories.models import Project, Story
from stories.forms import ProjectForm, StoryForm


@login_required
def index(request):
    projects = Project.objects.filter(active=True)
    context = RequestContext(request, {
        'projects':projects,
        'form':ProjectForm(),
    })
    return render_to_response('index.html', context)

@login_required
@permission_required('stories.add_project', login_url='/login/')
def add_project(request):
    if request.method == 'POST':
        project = Project(active=True)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('stories_index')
        else:
            return add_project_error(request, form)
    else:
        raise Http404

@login_required
def add_project_error(request, form):
    context = RequestContext(request, {
        'projects':Project.objects.all(),
        'form':form,
    })
    return render_to_response('index.html', context)

@login_required
@permission_required('stories.delete_project', login_url='/login/')
def remove_project(request):
    if request.method == 'POST':
        try:
            delete_id = request.POST['delete_id']
        except KeyError:
            return redirect('stories_index')
        project = get_object_or_404(Project, id=delete_id)
        project.active = False
        project.save()
        return redirect('stories_index')
    else:
        raise Http404

@login_required
@permission_required('stories.change_project', login_url='/login/')
def project_page(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if not project.active:
        raise Http404
    try:
        error = request.session['error']
    except KeyError:
        error = None
    form = _get_form(request, error, 'add_error')
    edit_form = _get_form(request, error, 'edit_error')
    request.session['error'] = {}
    stories = Story.objects.filter(project_id=project.id)
    context = RequestContext(request, {
        'project':project,
        'stories':stories,
        'form':form,
        'edit_form':edit_form,
        'error':error['ref'] if error else '',
        'users':UserProxy.objects.all()
    })
    return render_to_response('project.html', context)

def _get_form(request, error, error_ref):
    try:
        if error['ref'] == error_ref:
            form = StoryForm(
                    initial={
                        'id':error['id'],
                        'name':error['name'],
                        'time':error['time'],
                        'user':error['user'],
                        }
                    )
        else:
            form = StoryForm()
    except (TypeError, KeyError):
        form = StoryForm()
    return form

@login_required
@permission_required('stories.change_story', login_url='/login/')
def change_story_time(request):
    if request.method == 'POST':
        try:
            story_id = request.POST['id']
        except KeyError:
            raise Http404
        story = get_object_or_404(Story, id=story_id)
        try:
            time = request.POST['time']
        except KeyError:
            return redirect('project_page', project_id=story.project_id)
        story.time = time
        try:
            story.save()
        except Exception:
            request.session['error'] = {
                'ref':'change_story_error',
                'name':request.POST.get('name', ''),
                'time':request.POST.get('time', ''),
                'user':request.POST.get('user', ''),
            }
            return redirect('project_page', project_id=story.project_id)
        return redirect('project_page', project_id=story.project_id)
    else:
        raise Http404

@login_required
@permission_required('stories.add_story', login_url='/login/')
def add_story(request):
    if request.method == 'POST':
        story = Story(accepted=True)
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect('project_page', project_id=story.project_id)
        else:
            request.session['error'] = {
                'ref':'add_error',
                'name':request.POST.get('name', ''),
                'time':request.POST.get('time', ''),
                'user':request.POST.get('user', ''),
            }
            return redirect('project_page', project_id=request.POST['project'])
    else:
        raise Http404

@login_required
@permission_required('stories.delete_story', login_url='/login/')
def remove_story(request):
    if request.method == 'POST':
        try:
            delete_id = request.POST['delete_id']
        except KeyError:
            return redirect('stories_index')
        story = get_object_or_404(Story, id=delete_id)
        project_id = story.project_id
        story.delete()
        return redirect('project_page', project_id=project_id)
    else:
        raise Http404

@login_required
@permission_required('stories.change_story', login_url='/login/')
def edit_story(request):
    if request.method == 'POST':
        edit_id = request.POST.get('id', 0)
        try:
            story = Story.objects.get(id=edit_id)
        except Story.DoesNotExist:
            raise Http404
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect('project_page', project_id=story.project_id)
        else:
            request.session['error'] = {
                'ref':'edit_error',
                'id':request.POST.get('id', ''),
                'name':request.POST.get('name', ''),
                'time':request.POST.get('time', ''),
                'user':request.POST.get('user', ''),
            }
            return redirect('project_page', project_id=request.POST['project'])
    else:
        raise Http404
