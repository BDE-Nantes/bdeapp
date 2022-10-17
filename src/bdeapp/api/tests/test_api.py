from django.urls import reverse

from rest_framework.test import APITestCase

from bdeapp.challenges.models import FamilyStatus
from bdeapp.challenges.tests.factories import ChallengeFactory
from bdeapp.events.tests.factories import EventFactory
from bdeapp.families.tests.factories import FamilyFactory


class APITests(APITestCase):
    def test_filter_published(self):
        event_published = EventFactory()
        event_unpublished = EventFactory(published=False)

        data = self.client.get(reverse("api:event-list")).json()

        self.assertEqual(len(data), 1)

    def test_families_score(self):
        family = FamilyFactory()
        challenge_1 = ChallengeFactory(points=10, max_validations=1)
        challenge_2 = ChallengeFactory(points=15, max_validations=2)

        family_status_1 = FamilyStatus(
            family=family, challenge=challenge_1, validations=1
        )
        family_status_2 = FamilyStatus(
            family=family, challenge=challenge_2, validations=2
        )
        family_status_1.save()
        family_status_2.save()

        data = self.client.get(reverse("api:family-list")).json()

        self.assertEqual(data[0]["points"], 40)
