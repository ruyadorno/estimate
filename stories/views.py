from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
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
            return HttpResponseRedirect('/stories')
        else:
            return add_error(request, form)

def add_error(request, form):
    context = RequestContext(request, {'projects':Project.objects.all(), 'form':form})
    return render_to_response('index.html', context)
