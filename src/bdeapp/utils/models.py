import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class PublishedMixin(models.Model):
    published = models.BooleanField(_("Published"), default=True)

    class Meta:
        abstract = True


class UuidMixin(models.Model):
    uuid = models.UUIDField(
        _("Uuid"), help_text=_("Unique identifier (UUID4)"), default=uuid.uuid4
    )

    class Meta:
        abstract = True
