import factory

from bdeapp.siteconfig.models import RedirectLink


class RedirectLinkFactory(factory.django.DjangoModelFactory):
    url_slug = factory.Faker("slug")
    url = factory.Faker("url")

    class Meta:
        model = RedirectLink
