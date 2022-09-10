from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    promotion = models.CharField(
        _("promotion"),
        max_length=30,
        help_text=_("Promotion of the user."),
        blank=True,
        null=True,
    )
