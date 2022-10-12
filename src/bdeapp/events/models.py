from django.db import models
from django.utils.translation import gettext_lazy as _

from bdeapp.utils.models import PublishedMixin, UuidMixin


class Event(PublishedMixin, UuidMixin):
    name = models.CharField(_("Name"), max_length=50)
    date = models.DateField(verbose_name=_("Event date"))
    time = models.TimeField(verbose_name=_("Event time"), blank=True, null=True)
    description = models.TextField(_("Description"), max_length=85)
    long_description = models.TextField(_("Long description"), max_length=230)

    facebook_link = models.URLField(_("Facebook link"), null=True, blank=True)
    instagram_link = models.URLField(_("Instagram link"), null=True, blank=True)
    maps_link = models.URLField(_("Google Maps link"), null=True, blank=True)
    misc_link = models.URLField(_("Miscellaneous link"), null=True, blank=True)

    class Meta(PublishedMixin.Meta):
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ["-date", "-time"]

    def __str__(self) -> str:
        return f"{self.name} ({self.date})"
