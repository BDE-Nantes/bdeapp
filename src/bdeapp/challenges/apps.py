from django.apps import AppConfig


class ChallengesConfig(AppConfig):
    name = "bdeapp.challenges"

    def ready(self):
        from . import signals  # noqa
