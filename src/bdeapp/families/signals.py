from django.db.models.signals import post_save
from django.dispatch import receiver

from bdeapp.challenges.models import Challenge, FamilyStatus
from bdeapp.families.models import Family


@receiver(post_save, sender=Family)
def update_challenges(sender, **kwargs):
    """Signal receiver used to update challenges when a new
    family is created.
    """
    if kwargs.get("created"):
        for challenge in Challenge.objects.all():
            family_status = FamilyStatus(
                challenge=challenge, family=kwargs.get("instance")
            )
            family_status.save()
