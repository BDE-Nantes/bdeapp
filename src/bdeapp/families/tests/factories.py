import factory

from bdeapp.families.models import Family


class FamilyFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"family-{n}")
    image = factory.django.ImageField(width=500, height=500)

    class Meta:
        model = Family
