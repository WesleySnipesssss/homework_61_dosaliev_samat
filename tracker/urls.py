from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<int:pk>/issue/create/', views.IssueCreateView.as_view(), name='issue-create'),
    path('issue/<int:pk>/', views.IssueDetailView.as_view(), name='issue-detail'),
    path('issue/<int:pk>/edit/', views.IssueUpdateView.as_view(), name='issue-update'),
    path('issue/<int:pk>/delete/', views.IssueDeleteView.as_view(), name='issue-delete'),
]
