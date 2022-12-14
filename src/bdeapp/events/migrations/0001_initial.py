# Generated by Django 3.2.15 on 2022-09-10 19:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
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
                    "published",
                    models.BooleanField(default=True, verbose_name="Published"),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        help_text="Unique identifier (UUID4)",
                        verbose_name="Uuid",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
                ("date", models.DateField(verbose_name="Event date")),
                (
                    "time",
                    models.TimeField(blank=True, null=True, verbose_name="Event time"),
                ),
                (
                    "description",
                    models.TextField(max_length=85, verbose_name="Description"),
                ),
                (
                    "long_description",
                    models.TextField(max_length=230, verbose_name="Long description"),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
                "ordering": ["-date", "-time"],
                "abstract": False,
            },
        ),
    ]
