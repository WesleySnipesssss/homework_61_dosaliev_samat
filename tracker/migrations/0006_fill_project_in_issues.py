from django.db import migrations

def fill_project_for_existing_issues(apps, schema_editor):
    Project = apps.get_model('tracker', 'Project')
    Issue = apps.get_model('tracker', 'Issue')

    project = Project.objects.create(
        name="Тестовый проект",
        start_date="2024-01-01",
        description="Проект, созданный для заполнения существующих задач."
    )

    Issue.objects.filter(project__isnull=True).update(project=project)

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_project_issue_project'),
    ]

    operations = [
        migrations.RunPython(fill_project_for_existing_issues),
    ]
