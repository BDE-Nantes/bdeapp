import fnmatch

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

import magic

from bdeapp.challenges.models import Challenge, FamilyStatus, Proof
from bdeapp.families.models import Family

from .forms import (
    ChallengeAdminForm,
    FamilyStatusInlineForm,
    FamilyStatusInlineFormSet,
    ProofAdminForm,
)


class FamilyStatusInline(admin.TabularInline):
    model = FamilyStatus
    can_delete = False
    formset = FamilyStatusInlineFormSet
    form = FamilyStatusInlineForm

    def get_min_num(self, *args, **kwargs) -> int:
        return Family.objects.count()

    def get_max_num(self, *args, **kwargs) -> int:
        return Family.objects.count()


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    inlines = [FamilyStatusInline]
    list_display = ("name", "points", "description")
    list_filter = ("points",)
    readonly_fields = ("uuid",)
    fields = ("uuid", "name", "description", "points", "max_validations")
    search_fields = ("name", "description")
    form = ChallengeAdminForm


@admin.register(Proof)
class ProofAdmin(admin.ModelAdmin):
    list_display = ("family", "challenge", "status")
    list_filter = ("family", "status")
    readonly_fields = ("uuid", "preview_proof_content")
    fieldsets = (
        (
            None,
            {
                "fields": ("uuid", "family", "challenge", "name"),
            },
        ),
        (_("Status"), {"fields": ("status", "published")}),
        (_("Proof"), {"fields": ("proof_content", "preview_proof_content")}),
    )

    search_fields = ("challenge__name", "family__name")
    form = ProofAdminForm

    def preview_proof_content(self, obj):
        file_content_type = magic.from_buffer(obj.proof_content.read(2048), mime=True)
        obj.proof_content.seek(0)

        if fnmatch.fnmatch(file_content_type.lower(), "image/*"):
            return mark_safe(f'<img src="{obj.proof_content.url}" width="400" />')
        elif fnmatch.fnmatch(file_content_type.lower(), "video/*"):
            return mark_safe(
                f'<video src={obj.proof_content.url} width="400" controls />'
            )

    preview_proof_content.short_description = _("Preview proof content")
