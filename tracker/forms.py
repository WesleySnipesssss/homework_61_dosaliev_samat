from django import forms
from .models import Issue, Type, Project

class IssueForm(forms.ModelForm):
    types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'types']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date', 'description']

class IssueCreateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['description', 'status', 'project']