import functools

from django.core.validators import validate_image_file_extension
from django.db import models
from django.db.models import F, Sum
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from bdeapp.challenges.models import FamilyStatus
from bdeapp.siteconfig.models import SiteConfiguration
from bdeapp.utils.models import UuidMixin
from bdeapp.utils.storage import uuid_path
from bdeapp.utils.validators import ImageSizeValidator


class Family(UuidMixin):
    name = models.CharField(_("Name"), max_length=50, unique=True)
    image = models.ImageField(
        _("Image"),
        upload_to=functools.partial(uuid_path, suffix="families/", from_instance=True),
        validators=[validate_image_file_extension, ImageSizeValidator(500, 500)],
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Family")
        verbose_name_plural = _("Families")

    def __str__(self) -> str:
        return self.name

    @classmethod
    def can_add_family(cls) -> bool:
        return cls.objects.count() < SiteConfiguration.get_solo().max_families

    @property
    def points(self) -> int:
        return (
            FamilyStatus.objects.filter(family=self)
            .annotate(total_points=F("validations") * F("challenge__points"))
            .aggregate(Sum("total_points"))["total_points__sum"]
        )

    def clean(self):
        if not self.can_add_family():
            raise ValidationError(
                _("You have reached the maximum number of families allowed (%(max)s)"),
                params={"max": SiteConfiguration.get_solo().max_families},
            )
        return super().clean()

    def save(self, *args, **kwargs):
        if not self.can_add_family():
            return
        return super().save(*args, **kwargs)
