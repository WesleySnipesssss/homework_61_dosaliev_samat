from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue

class IssueListView(ListView):
    model = Issue
    template_name = 'tracker/issue_list.html'

class IssueDetailView(DetailView):
    model = Issue
    template_name = 'tracker/issue_detail.html'

class IssueCreateView(CreateView):
    model = Issue
    fields = ['summary', 'description', 'status', 'type']
    template_name = 'tracker/issue_form.html'
    success_url = reverse_lazy('issue_list')

class IssueUpdateView(UpdateView):
    model = Issue
    fields = ['summary', 'description', 'status', 'type']
    template_name = 'tracker/issue_form.html'
    success_url = reverse_lazy('issue_list')

class IssueDeleteView(DeleteView):
    model = Issue
    template_name = 'tracker/issue_confirm_delete.html'
    success_url = reverse_lazy('issue_list')
