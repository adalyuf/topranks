# Generated by Django 4.1.7 on 2023-04-08 14:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0015_keyword_alter_template_project_keywordpositions"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="KeywordPositions",
            new_name="KeywordPosition",
        ),
    ]