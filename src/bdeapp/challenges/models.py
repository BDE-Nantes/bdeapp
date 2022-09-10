import functools

from django.db import models
from django.utils.translation import gettext_lazy as _

from bdeapp.utils.models import UuidMixin
from bdeapp.utils.storage import uuid_path
from bdeapp.utils.validators import FileValidator


class FamilyStatus(models.Model):
    family = models.ForeignKey(
        "families.Family", verbose_name=_("Family"), on_delete=models.CASCADE
    )
    challenge = models.ForeignKey(
        "Challenge",
        verbose_name=_("Challenge"),
        related_name="families_status",
        on_delete=models.CASCADE,
    )
    validations = models.PositiveIntegerField(
        _("Validations"), help_text=_("Number of validations"), default=0
    )
    enabled = models.BooleanField(_("Enabled"), default=True)

    class Meta:
        verbose_name = _("Family status")
        verbose_name_plural = _("Families status")
        constraints = [
            models.UniqueConstraint(
                fields=["family", "challenge"], name="unique_challenge_family"
            )
        ]

    def clean(self):
        if not self.enabled:
            self.validations = 0


class Challenge(UuidMixin):
    name = models.CharField(_("Name"), max_length=70, unique=True)
    description = models.TextField(
        _("Description"),
        max_length=140,
        help_text=_("A short text describing the challenge"),
        blank=True,
        null=True,
    )
    points = models.PositiveIntegerField(_("Points"))

    class Meta:
        ordering = ["points", "name"]
        verbose_name = _("Challenge")
        verbose_name_plural = _("Challenges")

    def __str__(self) -> str:
        return self.name


class Proof(UuidMixin):
    class ProofStatus(models.TextChoices):
        PENDING = "PE", _("Pending")
        APPROVED = "AP", _("Approved")
        REJECTED = "RE", _("Rejected")

    family = models.ForeignKey(
        "families.Family", verbose_name=_("Family"), on_delete=models.CASCADE
    )
    challenge = models.ForeignKey(
        Challenge, verbose_name=_("Challenge"), on_delete=models.CASCADE
    )
    name = models.CharField(
        _("Name"),
        max_length=25,
        blank=True,
        null=True,
        help_text=_("Name of the user doing the challenge"),
    )
    status = models.CharField(
        _("Status"),
        max_length=2,
        choices=ProofStatus.choices,
        default=ProofStatus.PENDING,
    )
    published = models.BooleanField(
        _("Published"),
        default=False,
        help_text=_("Whether the proof is displayed on the website."),
    )

    proof_content = models.FileField(
        _("Proof content"),
        upload_to=functools.partial(uuid_path, suffix="proofs/"),
        validators=[
            FileValidator(
                max_size=1024 * 1024 * 100, content_types=["video/*", "image/*"]
            )
        ],
    )

    class Meta:
        verbose_name = _("Proof")
        verbose_name_plural = _("Proofs")

    def __str__(self) -> str:
        return f"{self.family} - {self.challenge}"

    def get_status(self) -> ProofStatus:
        return self.ProofStatus(self.status)
