from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import FamilyStatus, Proof


@receiver(pre_save, sender=Proof)
def save_old_instance(sender: type[Proof], instance: Proof, **kwargs):
    try:
        instance._old_status = sender.objects.get(pk=instance.pk).get_status()
    except sender.DoesNotExist:
        pass


@receiver(post_save, sender=Proof)
def update_family_status_on_approved(sender: type[Proof], instance: Proof, **kwargs):
    """Signal receiver used to update family status
    when the proof gets approved.
    """
    family_status = FamilyStatus.objects.get(
        family=instance.family, challenge=instance.challenge
    )
    if kwargs.get("created"):
        if instance.get_status() is Proof.ProofStatus.APPROVED:
            family_status.validations += 1
    else:
        if (
            instance._old_status is not Proof.ProofStatus.APPROVED
            and instance.get_status() is Proof.ProofStatus.APPROVED
        ):
            family_status.validations += 1
        if (
            instance._old_status is Proof.ProofStatus.APPROVED
            and instance.get_status() is not Proof.ProofStatus.APPROVED
            and family_status.validations > 0
        ):
            family_status.validations -= 1
        family_status.save()


@receiver(post_delete, sender=Proof)
def update_family_status_on_deleted(sender: type[Proof], instance: Proof, **kwargs):
    """Signal receiver used to update family status
    when a proof gets deleted.
    """
    family_status = FamilyStatus.objects.get(
        family=instance.family, challenge=instance.challenge
    )
    if (
        instance.get_status() is Proof.ProofStatus.APPROVED
        and family_status.validations > 0
    ):
        family_status.validations -= 1
        family_status.save()
