from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import now
from django.urls import reverse

def validate_summary_length(value):
    if len(value) > 100:
        raise ValidationError("Название задачи не должно превышать 100 символов.")

def validate_due_date(value):
    if value < timezone.now().date():
        raise ValidationError("Дата завершения задачи не может быть в прошлом.")

class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания", null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", default=now)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})


class Issue(models.Model):
    summary = models.CharField(max_length=100, validators=[validate_summary_length])
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=False, blank=False)
    types = models.ManyToManyField(Type, related_name="issues", verbose_name="Типы")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, editable=False)
    due_date = models.DateField(validators=[validate_due_date], blank=True, null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Проект"
    )

    def __str__(self):
        return self.summary

    def get_absolute_url(self):
        return reverse('issue-detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        ordering = ['-created_at']

