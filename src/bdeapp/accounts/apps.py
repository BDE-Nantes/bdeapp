from io import StringIO

from django.apps import AppConfig
from django.core.management import call_command
from django.db.models.signals import post_migrate


def update_schools(sender, **kwargs):
    from bdeapp.siteconfig.models import School

    School.objects.all().delete()

    call_command(
        "loaddata", "default_schools", verbosity=0, stdout=StringIO(), stderr=StringIO()
    )


class AccountsConfig(AppConfig):
    name = "bdeapp.accounts"

    def ready(self):
        post_migrate.connect(update_schools, sender=self)
