# Generated by Django 4.2.1 on 2023-06-29 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0017_rename_newbrand_brand"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="NewBrandDomain",
            new_name="BrandDomain",
        ),
    ]
