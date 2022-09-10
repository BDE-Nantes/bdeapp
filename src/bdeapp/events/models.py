from django.db import models
from django.utils.translation import gettext_lazy as _

from bdeapp.utils.models import PublishedMixin, UuidMixin


class Event(PublishedMixin, UuidMixin):
    name = models.CharField(_("Name"), max_length=50)
    date = models.DateField(verbose_name=_("Event date"))
    time = models.TimeField(verbose_name=_("Event time"), blank=True, null=True)
    description = models.TextField(_("Description"), max_length=85)
    long_description = models.TextField(_("Long description"), max_length=230)

    class Meta(PublishedMixin.Meta):
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ["-date", "-time"]

    def __str__(self) -> str:
        return f"{self.name} ({self.date})"
