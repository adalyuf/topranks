# Generated by Django 4.1.7 on 2023-04-02 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0005_aimodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="conversation",
            name="ai_model",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="ranker.aimodel",
            ),
            preserve_default=False,
        ),
    ]
