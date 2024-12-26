from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, Issue
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm

class ProjectListView(ListView):
    model = Project
    template_name = 'tracker/project_list.html'
    context_object_name = 'project_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = Project.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
        return queryset

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'tracker/project_detail.html'
    context_object_name = 'project'

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'tracker/project_form.html'
    fields = ['name', 'start_date', 'end_date', 'description']

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'tracker/project_form.html'
    fields = ['name', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'tracker/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class IssueCreateView(CreateView):
    model = Issue
    template_name = 'tracker/issue_form.html'
    fields = ['summary', 'description', 'status', 'types', 'type']

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['pk'])
        if not form.cleaned_data['type']:
            form.instance.type = form.cleaned_data['types'].first()
        response = super().form_valid(form)
        if 'types' in form.cleaned_data:
            form.instance.types.set(form.cleaned_data['types'])

        return response

class IssueDetailView(DetailView):
    model = Issue
    template_name = 'tracker/issue_detail.html'
    context_object_name = 'issue'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Issue, pk=self.kwargs['pk'])
        if obj.is_deleted:
            raise Http404("Задача не найдена.")
        return obj

class IssueUpdateView(UpdateView):
    model = Issue
    fields = ['summary', 'description']
    template_name = 'tracker/issue_form.html'
    context_object_name = 'issue'

    def get_success_url(self):
        return reverse_lazy('issue-detail', kwargs={'pk': self.object.pk})

class IssueDeleteView(DeleteView):
    model = Issue
    template_name = 'tracker/issue_confirm_delete.html'
    context_object_name = 'issue'
    success_url = reverse_lazy('project-detail')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return self.get(self, request, *args, **kwargs)

    def get_success_url(self):
        project = self.object.project
        return reverse_lazy('project-detail', kwargs={'pk': project.pk})

def issue_list(request):
    issues = Issue.objects.filter(is_deleted=False)
    return render(request, 'tracker/issue_list.html', {'issues': issues})

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project-list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

@login_required
def edit_project(request, pk):
    project = Project.objects.get(pk=pk)
    if project.author != request.user:
        return redirect('project-list')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project-list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'project_edit.html', {'form': form})

@login_required
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    if project.author != request.user:
        return redirect('project-list')
    if request.method == 'POST':
        project.delete()
        return redirect('project-list')

    return render(request, 'project_confirm_delete.html', {'project': project})