from django import forms

from stories.models import Project, Story


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('active',)

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('accepted',)
