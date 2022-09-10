from django.conf import settings as django_settings


def settings(request):
    public_settings = ()

    context = {
        "settings": {k: getattr(django_settings, k, None) for k in public_settings}
    }

    return context
