import os

os.environ.setdefault("DEBUG", "yes")
os.environ.setdefault("ALLOWED_HOSTS", "*")
os.environ.setdefault(
    "SECRET_KEY",
    "django-insecure-fn2%nip&mi+y$86v%nyp&x=tx))5hhx+%bk53zklyet5ux%48p",
)
os.environ.setdefault("IS_HTTPS", "no")
os.environ.setdefault("VERSION_TAG", "dev")

os.environ.setdefault("DB_NAME", "bdeapp"),
os.environ.setdefault("DB_USER", "bdeapp"),
os.environ.setdefault("DB_PASSWORD", "bdeapp"),

os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("TWO_FACTOR_FORCE_OTP_ADMIN", "no")
os.environ.setdefault("TWO_FACTOR_PATCH_ADMIN", "no")

from .base import *  # noqa isort:skip

# Feel free to switch dev to sqlite3 for simple projects,
# os.environ.setdefault("DB_ENGINE", "django.db.backends.sqlite3")

#
# Standard Django settings.
#
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING["loggers"].update(
    {
        "bdeapp": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["django"],
            "level": "DEBUG",
            "propagate": False,
        },
        "performance": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        #
        # See: https://code.djangoproject.com/ticket/30554
        # Autoreload logs excessively, turn it down a bit.
        #
        "django.utils.autoreload": {
            "handlers": ["django"],
            "level": "INFO",
            "propagate": False,
        },
    }
)

SESSION_ENGINE = "django.contrib.sessions.backends.db"

# in memory cache and django-axes don't get along.
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#known-configuration-problems
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "axes": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}


INTERNAL_IPS = ("127.0.0.1",)


# Override settings with local settings.
try:
    from .local import *  # noqa
except ImportError:
    pass
