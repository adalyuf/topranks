# Generated by Django 4.2.1 on 2023-06-28 13:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0010_brand_keyword_indexed_at_brandkeyword_brand_keyword"),
    ]

    operations = [
        migrations.AddField(
            model_name="brand",
            name="indexing_requested_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
