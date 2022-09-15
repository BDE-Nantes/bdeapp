from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase

from bdeapp.challenges.models import FamilyStatus, Proof
from bdeapp.challenges.tests.factories import ChallengeFactory, ProofFactory
from bdeapp.families.tests.factories import FamilyFactory
from bdeapp.siteconfig.models import SiteConfiguration


class TestModelValidation(TestCase):
    def test_status_max_validations(self):
        site_configuration = SiteConfiguration(max_families=1)
        site_configuration.save()

        family = FamilyFactory()
        challenge = ChallengeFactory(max_validations=1)
        family_status = FamilyStatus(family=family, challenge=challenge, validations=2)

        self.assertRaises(ValidationError, family_status.clean)

    def test_status_constraint(self):
        family = FamilyFactory()
        challenge = ChallengeFactory()

        family_status_1 = FamilyStatus(family=family, challenge=challenge)
        family_status_1.save()

        family_status_2 = FamilyStatus(family=family, challenge=challenge)
        self.assertRaises(IntegrityError, family_status_2.save)

    def test_status_disabled(self):
        family = FamilyFactory()
        challenge = ChallengeFactory()

        family_status = FamilyStatus(
            family=family, challenge=challenge, validations=1, enabled=False
        )
        family_status.save()

        self.assertEqual(family_status.validations, 0)

    def test_proof_max_validations(self):
        family = FamilyFactory()
        challenge = ChallengeFactory(max_validations=1)

        family_status = FamilyStatus(family=family, challenge=challenge, validations=1)
        family_status.save()

        proof = ProofFactory(family=family, challenge=challenge)

        proof.status = Proof.ProofStatus.APPROVED

        self.assertRaises(ValidationError, proof.clean)

    def test_proof_max_validations_new(self):
        family = FamilyFactory()
        challenge = ChallengeFactory(max_validations=1)

        family_status = FamilyStatus(family=family, challenge=challenge, validations=1)
        family_status.save()

        proof = ProofFactory.build(
            family=family, challenge=challenge, status=Proof.ProofStatus.APPROVED
        )

        self.assertRaises(ValidationError, proof.clean)
