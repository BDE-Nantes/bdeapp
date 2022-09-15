import factory

from bdeapp.challenges.models import Challenge, Proof
from bdeapp.families.tests.factories import FamilyFactory


class ChallengeFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"challenge-{n}")
    points = factory.Faker("random_digit_not_null")
    max_validations = factory.Faker("random_digit_not_null")

    class Meta:
        model = Challenge


class ProofFactory(factory.django.DjangoModelFactory):
    family = factory.SubFactory(FamilyFactory)
    challenge = factory.SubFactory(ChallengeFactory)
    proof_content = factory.django.ImageField(width=500, height=500)

    class Meta:
        model = Proof
