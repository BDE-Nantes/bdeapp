from django.forms import ValidationError
from django.test import TestCase

from bdeapp.families.models import Family
from bdeapp.families.tests.factories import FamilyFactory
from bdeapp.siteconfig.models import SiteConfiguration


class TestModelValidation(TestCase):
    def test_max_families(self):
        site_configuration = SiteConfiguration(max_families=1)
        site_configuration.save()
        self.assertTrue(Family.can_add_family())
        FamilyFactory()
        self.assertFalse(Family.can_add_family())
        family_2 = Family()
        self.assertRaises(ValidationError, family_2.clean)
