from django.forms import ModelForm

from stories.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ('active',)
