# Generated by Django 4.1.7 on 2023-05-09 14:49

import django.core.validators
from django.db import migrations, models
import ranker.models


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="keywordfile",
            name="filepath",
            field=models.FileField(
                upload_to=ranker.models.keyword_directory_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["csv"]
                    )
                ],
            ),
        ),
    ]
