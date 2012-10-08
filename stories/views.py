from django.http import Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from stories.models import Project, Story
from stories.forms import ProjectForm, StoryForm


def index(request):
    context = RequestContext(request, {'projects':Project.objects.all(), 'form':ProjectForm()})
    return render_to_response('index.html', context)

def add_project(request):
    if request.method == 'POST':
        project = Project(active=True)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('stories_index')
        else:
            return add_project_error(request, form)

def add_project_error(request, form):
    context = RequestContext(request, {'projects':Project.objects.all(), 'form':form})
    return render_to_response('index.html', context)

def remove_project(request):
    if request.method == 'POST':
        try:
            delete_id = request.POST['delete_id']
        except KeyError:
            return redirect('stories_index')
        project = get_object_or_404(Project, id=delete_id)
        project.delete()
        return redirect('stories_index')
    else:
        raise Http404

def project_page(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    stories = Story.objects.filter(project_id=project.id)
    context = RequestContext(request, {'project':project, 'stories':stories, 'form':StoryForm})
    return render_to_response('project.html', context)

def change_story_time(request):
    if request.method == 'POST':
        try:
            story_id = request.POST['id']
        except KeyError:
            return redirect('stories_index')
        story = get_object_or_404(Story, id=story_id)
        try:
            time = request.POST['time']
        except KeyError:
            return redirect('project_page', project_id=story.project_id)
        story.time = time
        try:
            story.save()
        except Exception:
            #TODO: Return to the project page adding a custom error message
            #Actually, that would be a nice behaviour for add/remove actions
            pass
        return redirect('project_page', project_id=story.project_id)
    else:
        raise Http404

def add_story(request):
    if request.method == 'POST':
        story = Story(accepted=True)
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect('project_page', project_id=story.project_id)
        else:
            #TODO: Return to project page with an error here too
            raise Http404
    else:
        raise Http404
