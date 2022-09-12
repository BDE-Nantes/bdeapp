# Generated by Django 3.2.15 on 2022-09-11 19:41

import bdeapp.challenges.models
import bdeapp.utils.storage
import bdeapp.utils.validators
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ("challenges", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proof",
            name="proof_content",
            field=models.FileField(
                upload_to=functools.partial(
                    bdeapp.utils.storage.uuid_path, *(), **{"suffix": "proofs/"}
                ),
                validators=[
                    bdeapp.utils.validators.FileValidator(
                        content_types=["video/*", "image/*"],
                        max_size=bdeapp.challenges.models.get_max_file_size,
                    )
                ],
                verbose_name="Proof content",
            ),
        ),
    ]