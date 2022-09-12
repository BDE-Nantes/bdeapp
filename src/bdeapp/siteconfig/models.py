from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel


class SiteConfiguration(SingletonModel):
    max_families = models.PositiveIntegerField(
        _("Maximum number of families"), default=5
    )

    max_proof_filesize = models.PositiveIntegerField(
        _("Maximum proof file size (MB)"), default=100
    )

    class Meta:
        verbose_name = _("Site configuration")

    def __str__(self) -> str:
        return "Site Configuration"

    def clean(self):
        from bdeapp.families.models import Family

        if (nb_families := Family.objects.count()) > self.max_families:
            raise ValidationError(
                _("You have too much family instances (%(nb_families)s)"),
                params={"nb_families": nb_families},
            )