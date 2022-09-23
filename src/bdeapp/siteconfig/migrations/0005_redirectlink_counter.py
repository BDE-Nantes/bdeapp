# Generated by Django 3.2.15 on 2022-09-23 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("siteconfig", "0004_alter_redirectlink_url_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="redirectlink",
            name="counter",
            field=models.PositiveIntegerField(
                default=0, help_text="Number of visits", verbose_name="Visits"
            ),
        ),
    ]
