# Generated by Django 4.1.7 on 2023-04-02 13:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0007_project_template_helper_text_after_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="requests_users",
            new_name="requests_used",
        ),
    ]