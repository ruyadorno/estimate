from django.shortcuts import render_to_response
from django.template import RequestContext

from stories.models import Project


def index(request):
    context = RequestContext(request, {'projects':Project.objects.all()})
    return render_to_response('index.html', context)
