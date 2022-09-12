from django.apps import AppConfig
from django.db.backends.signals import connection_created


def init_site_config(*args, **kwargs):
    from .models import SiteConfiguration

    SiteConfiguration.get_solo()


class SiteconfigConfig(AppConfig):
    name = "bdeapp.siteconfig"

    def ready(self):
        connection_created.connect(init_site_config, sender=self)
