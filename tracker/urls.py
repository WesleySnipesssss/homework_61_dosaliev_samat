from django.urls import path
from . import views

urlpatterns = [
    path('', views.IssueListView.as_view(), name='issue_list'),
    path('<int:pk>/', views.IssueDetailView.as_view(), name='issue_detail'),
    path('add/', views.IssueCreateView.as_view(), name='issue_add'),
    path('<int:pk>/edit/', views.IssueUpdateView.as_view(), name='issue_edit'),
    path('<int:pk>/delete/', views.IssueDeleteView.as_view(), name='issue_delete'),
]
