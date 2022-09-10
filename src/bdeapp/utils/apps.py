from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "bdeapp.utils"

    def ready(self):
        from . import checks  # noqa
