# Generated by Django 4.2.1 on 2023-06-29 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0013_newbrand"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewBrandDomain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("brand", "brand"),
                            ("product", "product"),
                            ("competitor_brand", "competitor_brand"),
                            ("competitor_product", "competitor_product"),
                        ],
                        default="brand",
                        max_length=200,
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ranker.newbrand",
                    ),
                ),
                (
                    "domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ranker.domain"
                    ),
                ),
            ],
        ),
    ]