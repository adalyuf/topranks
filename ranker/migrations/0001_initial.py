# Generated by Django 4.1.7 on 2023-03-28 17:48

from django.db import migrations, models
import django.db.models.deletion
import ranker.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Conversation",
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
                ("requested_at", models.DateTimeField(null=True)),
                ("answered_at", models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Domain",
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
                ("domain", models.CharField(max_length=200, unique=True)),
                ("keywords", models.BigIntegerField(null=True)),
                ("traffic", models.BigIntegerField(null=True)),
                (
                    "cost",
                    models.DecimalField(decimal_places=2, max_digits=19, null=True),
                ),
                ("rank", models.IntegerField(null=True)),
                ("ad_keywords", models.BigIntegerField(null=True)),
                ("ad_traffic", models.BigIntegerField(null=True)),
                (
                    "ad_cost",
                    models.DecimalField(decimal_places=2, max_digits=19, null=True),
                ),
                ("adult_content", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("product", models.CharField(max_length=200, unique=True)),
                (
                    "scope",
                    models.CharField(
                        choices=[("global", "global"), ("per_domain", "per_domain")],
                        default="per_domain",
                        max_length=200,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TokenType",
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
                ("type", models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Token",
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
                ("value", models.CharField(max_length=200)),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ranker.tokentype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductTemplate",
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
                ("prompt1", models.TextField()),
                ("prompt2", models.CharField(blank=True, max_length=200, null=True)),
                ("title", models.CharField(blank=True, max_length=200, null=True)),
                ("order", models.IntegerField(default=100)),
                ("visible", models.BooleanField(default=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ranker.product"
                    ),
                ),
                (
                    "token1",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="ranker.tokentype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
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
                ("prompt", models.TextField()),
                ("title", models.CharField(max_length=200, null=True)),
                ("response", models.TextField(null=True)),
                ("formatted_response", models.TextField(null=True)),
                ("visible", models.BooleanField(default=True)),
                ("order", models.IntegerField(default=100)),
                ("requested_at", models.DateTimeField(null=True)),
                ("answered_at", models.DateTimeField(null=True)),
                (
                    "conversation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ranker.conversation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="KeywordFile",
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
                    "filepath",
                    models.FileField(upload_to=ranker.models.keyword_directory_path),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("primary", models.BooleanField(default=False)),
                (
                    "domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ranker.domain"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="conversation",
            name="domain",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="ranker.domain",
            ),
        ),
        migrations.AddField(
            model_name="conversation",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ranker.product"
            ),
        ),
        migrations.AddConstraint(
            model_name="conversation",
            constraint=models.UniqueConstraint(
                fields=("product", "domain"),
                include=("answered_at",),
                name="unique_product_domain",
            ),
        ),
    ]
