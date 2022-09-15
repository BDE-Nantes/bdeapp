from django.urls import reverse

from rest_framework.test import APITestCase

from bdeapp.events.tests.factories import EventFactory


class APITests(APITestCase):
    def test_filter_published(self):
        event_published = EventFactory()
        event_unpublished = EventFactory(published=False)

        data = self.client.get(reverse("api:event-list")).json()

        self.assertEqual(len(data), 1)
