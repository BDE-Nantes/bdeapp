import functools

from django.core.validators import MinValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from bdeapp.events.models import Event
from bdeapp.siteconfig.models import SiteConfiguration
from bdeapp.utils.models import PublishedMixin, UuidMixin
from bdeapp.utils.storage import uuid_path
from bdeapp.utils.validators import FileValidator

MAX_VALIDATIONS_MINIMUM = 1


def get_max_file_size():
    return SiteConfiguration.get_solo().max_proof_filesize * 1024 * 1024


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
        if self.validations > self.challenge.max_validations:
            raise ValidationError(
                _("You have reached the maximum number of validations (%(max)s)."),
                params={"max": self.challenge.max_validations},
            )

    def save(self):
        if not self.enabled:
            self.validations = 0
        if self.validations > self.challenge.max_validations:
            return
        super().save()


class Challenge(PublishedMixin, UuidMixin):
    name = models.CharField(_("Name"), max_length=70, unique=True)
    description = models.TextField(
        _("Description"),
        max_length=140,
        help_text=_("A short text describing the challenge"),
        blank=True,
        null=True,
    )
    points = models.PositiveIntegerField(_("Points"))
    max_validations = models.PositiveIntegerField(
        _("Maximum number of validations"),
        default=1,
        validators=[MinValueValidator(limit_value=MAX_VALIDATIONS_MINIMUM)],
    )

    related_event = models.ForeignKey(
        Event,
        verbose_name=_("Related event"),
        limit_choices_to={"published": True},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    start_date = models.DateTimeField(_("Start date"), null=True, blank=True)

    end_date = models.DateTimeField(_("End date"), null=True, blank=True)

    class Meta:
        ordering = ["points", "name"]
        verbose_name = _("Challenge")
        verbose_name_plural = _("Challenges")

    def __str__(self) -> str:
        return self.name

    def clean(self):
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.end_date <= self.start_date
        ):
            raise ValidationError(
                {"end_date": _("End date must be after start date")},
                code="invalid_date",
            )


class Proof(UuidMixin):
    class ProofStatus(models.TextChoices):
        PENDING = "PE", _("Pending")
        APPROVED = "AP", _("Approved")
        REJECTED = "RE", _("Rejected")

    family = models.ForeignKey(
        "families.Family", verbose_name=_("Family"), on_delete=models.CASCADE
    )
    challenge = models.ForeignKey(
        Challenge,
        verbose_name=_("Challenge"),
        on_delete=models.CASCADE,
        limit_choices_to={"published": True},
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
                max_size=get_max_file_size, content_types=["video/*", "image/*"]
            )
        ],
    )

    class Meta:
        verbose_name = _("Proof")
        verbose_name_plural = _("Proofs")

    def __str__(self) -> str:
        return f"{self.family} - {self.challenge}"

    def clean(self):
        """Will ensure that an approved proof can be added
        by checking the maximum number of validations available.
        The FamilyStatus update is done in a post_save signal receiver.
        """
        can_add_validation = (
            FamilyStatus.objects.get(
                challenge=self.challenge, family=self.family
            ).validations
            < self.challenge.max_validations
        )

        if not can_add_validation:
            try:
                old_status = type(self).objects.get(pk=self.pk).get_status()
                error = (
                    old_status is not Proof.ProofStatus.APPROVED
                    and self.get_status() is Proof.ProofStatus.APPROVED
                )
            except type(self).DoesNotExist:
                error = self.get_status() is Proof.ProofStatus.APPROVED
            if error:
                raise ValidationError(
                    _(
                        "You have reached the maximum number of validations for this challenge (%(max)s)."
                    ),
                    params={"max": self.challenge.max_validations},
                    code="max_validations",
                )
        return super().clean()

    def get_status(self) -> ProofStatus:
        return self.ProofStatus(self.status)
