from django import forms

from stories.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('active',)
