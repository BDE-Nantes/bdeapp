from django.test import TestCase
from django.urls import reverse

from .factories import RedirectLinkFactory


class TestRedirectLink(TestCase):
    def test_redirect_link_found(self):
        redirect_link = RedirectLinkFactory()
        response = self.client.get(
            reverse("link_redirect", kwargs={"slug": redirect_link.url_slug}),
            follow=False,
        )
        self.assertRedirects(response, redirect_link.url, fetch_redirect_response=False)

    def test_redirect_link_not_found(self):
        RedirectLinkFactory()
        response = self.client.get(
            reverse("link_redirect", kwargs={"slug": "__non_existing_slug__"}),
            follow=False,
        )
        self.assertEqual(response.status_code, 404)
