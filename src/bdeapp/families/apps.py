from django.apps import AppConfig


class FamiliesConfig(AppConfig):
    name = "bdeapp.families"

    def ready(self):
        from . import signals  # noqa
