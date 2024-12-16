from django.utils import timezone
from datetime import timedelta
from .models import Issue
from django.db import models

def closed_issues_last_month():
    one_month_ago = timezone.now() - timedelta(days=30)
    issues = Issue.objects.filter(
        status__name="Closed",
        updated_at__gte=one_month_ago
    )
    return issues

def issues_with_status_and_type(statuses, types):
    issues = Issue.objects.filter(
        status__name__in=statuses,
        type__name__in=types
    )
    return issues

def unresolved_issues_with_bug():
    issues = Issue.objects.filter(
        status__name__in=["Open", "In Progress"],
    ).filter(
        models.Q(summary__icontains="bug") | models.Q(type__name="Баг")
    )
    return issues

def issues_selected_fields():
    issues = Issue.objects.values("id", "summary", "type__name", "status__name")
    return issues

def issues_with_matching_description():
    issues = Issue.objects.filter(
        description=models.F("summary")
    )
    return issues

def issue_count_by_type():
    issues = Issue.objects.values("type__name").annotate(count=models.Count("id"))
    return issues
