from django.urls import path
from .views import (
    IssueListView,
    IssueDetailView,
    IssueCreateView,
    IssueUpdateView,
    IssueDeleteView,
)

urlpatterns = [
    path('', IssueListView.as_view(), name='issue_list'),
    path('<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
    path('create/', IssueCreateView.as_view(), name='issue_create'),
    path('<int:pk>/update/', IssueUpdateView.as_view(), name='issue_update'),
    path('<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete'),
]