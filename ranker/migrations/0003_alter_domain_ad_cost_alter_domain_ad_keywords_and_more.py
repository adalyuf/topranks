# Generated by Django 4.1.7 on 2023-05-11 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ranker", "0002_alter_keywordfile_filepath"),
    ]

    operations = [
        migrations.AlterField(
            model_name="domain",
            name="ad_cost",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=19, null=True
            ),
        ),
        migrations.AlterField(
            model_name="domain",
            name="ad_keywords",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="domain",
            name="ad_traffic",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="domain",
            name="cost",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=19, null=True
            ),
        ),
        migrations.AlterField(
            model_name="domain",
            name="keywords",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="domain",
            name="rank",
            field=models.IntegerField(default=999999, null=True),
        ),
        migrations.AlterField(
            model_name="domain",
            name="traffic",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
