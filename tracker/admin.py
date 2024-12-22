from django.contrib import admin
from .models import Status, Type, Issue, Project

admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Issue)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)