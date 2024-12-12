from django import forms
from .models import Issue, Type

class IssueForm(forms.ModelForm):
    types = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'types']
