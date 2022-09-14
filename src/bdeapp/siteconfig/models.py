from django.db import models
from django.forms import ValidationError
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel

mark_safe_lazy = lazy(mark_safe, str)


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


class RedirectLink(models.Model):
    url_slug = models.SlugField(
        _("Url name"),
        help_text=mark_safe_lazy(
            _("Your url will be accessible from <code>/to/url_name/</code>")
        ),
        unique=True,
    )
    url = models.URLField(_("Redirect url"), help_text=_("Url to redirect to"))

    class Meta:
        verbose_name = _("Redirect link")
        verbose_name_plural = _("Redirect links")

    def __str__(self) -> str:
        return self.url_slug
