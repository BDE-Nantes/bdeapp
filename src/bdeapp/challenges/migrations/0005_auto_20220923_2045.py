# Generated by Django 3.2.15 on 2022-09-23 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
        ("challenges", "0004_alter_challenge_max_validations"),
    ]

    operations = [
        migrations.AddField(
            model_name="challenge",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="End date"),
        ),
        migrations.AddField(
            model_name="challenge",
            name="published",
            field=models.BooleanField(default=True, verbose_name="Published"),
        ),
        migrations.AddField(
            model_name="challenge",
            name="related_event",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"published": True},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.event",
                verbose_name="Related event",
            ),
        ),
        migrations.AddField(
            model_name="challenge",
            name="start_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Start date"
            ),
        ),
        migrations.AlterField(
            model_name="proof",
            name="challenge",
            field=models.ForeignKey(
                limit_choices_to={"published": True},
                on_delete=django.db.models.deletion.CASCADE,
                to="challenges.challenge",
                verbose_name="Challenge",
            ),
        ),
    ]