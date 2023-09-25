# Generated by Django 4.2.1 on 2023-09-21 15:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0033_alter_competition_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="keyword",
            name="category_scores",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="keyword",
            name="primary_category",
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
    ]
