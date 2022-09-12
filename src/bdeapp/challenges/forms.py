from typing import Literal

from django.contrib.admin.widgets import AdminIntegerFieldWidget
from django.forms import IntegerField
from django.forms.models import BaseInlineFormSet, ModelForm
from django.forms.widgets import ClearableFileInput

from bdeapp.challenges.models import (
    MAX_VALIDATIONS_MINIMUM,
    Challenge,
    FamilyStatus,
    Proof,
)
from bdeapp.families.models import Family


class FamilyStatusInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs) -> None:
        initial = [{"family": family.pk} for family in Family.objects.all()]
        kwargs.update({"initial": initial})
        super().__init__(*args, **kwargs)


class FamilyStatusInlineForm(ModelForm):
    def has_changed(self) -> Literal[True]:
        return True

    class Meta:
        model = FamilyStatus
        fields = ["family", "challenge", "validations", "enabled"]


class ChallengeAdminForm(ModelForm):
    max_validations = IntegerField(
        min_value=MAX_VALIDATIONS_MINIMUM, widget=AdminIntegerFieldWidget, initial=1
    )

    class Meta:
        model = Challenge
        fields = ["name", "description", "points", "max_validations"]


class ProofAdminForm(ModelForm):
    class Meta:
        model = Proof
        widgets = {
            "proof_content": ClearableFileInput(attrs={"accept": "video/*, image/*"})
        }
        fields = ["family", "challenge", "name", "status", "published", "proof_content"]
