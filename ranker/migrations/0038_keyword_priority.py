# Generated by Django 4.2.1 on 2023-10-02 19:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0037_remove_keyword_primary_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="keyword",
            name="priority",
            field=models.IntegerField(null=True),
        ),
    ]
