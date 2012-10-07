from django.http import Http404
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from stories.models import Project
from stories.forms import ProjectForm


def index(request):
    context = RequestContext(request, {'projects':Project.objects.all(), 'form':ProjectForm()})
    return render_to_response('index.html', context)

def add(request):
    if request.method == 'POST':
        project = Project(active=True)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('stories_index')
        else:
            return add_error(request, form)

def add_error(request, form):
    context = RequestContext(request, {'projects':Project.objects.all(), 'form':form})
    return render_to_response('index.html', context)

def remove(request):
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
