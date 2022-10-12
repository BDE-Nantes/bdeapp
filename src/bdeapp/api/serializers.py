from rest_framework import serializers

from bdeapp.challenges.models import Challenge, FamilyStatus, Proof
from bdeapp.events.models import Event
from bdeapp.families.models import Family
from bdeapp.siteconfig.models import School, SiteConfiguration


class EventSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField("get_links")

    def get_links(self, obj):
        return {
            k: getattr(obj, f"{k}_link")
            for k in ["facebook", "instagram", "maps", "misc"]
        }

    class Meta:
        model = Event
        fields = [
            "uuid",
            "published",
            "name",
            "date",
            "time",
            "description",
            "long_description",
            "links",
        ]


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ["uuid", "name", "image"]


class FamilyStatusSerializer(serializers.ModelSerializer):
    family = serializers.SlugRelatedField(slug_field="uuid", read_only=True)

    class Meta:
        model = FamilyStatus
        fields = ["family", "validations", "enabled"]


class ChallengeSerializer(serializers.ModelSerializer):
    families_status = FamilyStatusSerializer(many=True, read_only=True)
    related_event = serializers.SlugRelatedField(slug_field="uuid", read_only=True)

    class Meta:
        model = Challenge
        fields = [
            "uuid",
            "name",
            "description",
            "points",
            "max_validations",
            "families_status",
            "related_event",
            "start_date",
            "end_date",
        ]


class ProofSerializer(serializers.ModelSerializer):
    family = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Family.objects.all()
    )
    challenge = serializers.SlugRelatedField(
        slug_field="uuid", queryset=Challenge.objects.all()
    )

    class Meta:
        model = Proof
        fields = ["uuid", "family", "challenge", "name", "proof_content"]
        read_only_fields = ["uuid"]


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["name", "color"]


class SiteConfigurationSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)

    class Meta:
        model = SiteConfiguration
        fields = ["school"]
