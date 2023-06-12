# Generated by Django 4.2.1 on 2023-05-19 21:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0003_alter_domain_ad_cost_alter_domain_ad_keywords_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectdomain",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="ranker.project",
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Z0-9-_ ]+$",
                        "Only numbers, letters, underscores, dashes and spaces are allowed.",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="template",
            name="template",
            field=models.CharField(
                max_length=200,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Z0-9-_ ]+$",
                        "Only numbers, letters, underscores, dashes and spaces are allowed.",
                    )
                ],
            ),
        ),
    ]