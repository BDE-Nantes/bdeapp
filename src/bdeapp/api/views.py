from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from bdeapp.challenges.models import Challenge, Proof
from bdeapp.events.models import Event
from bdeapp.families.models import Family
from bdeapp.siteconfig.models import SiteConfiguration

from .serializers import (
    ChallengeSerializer,
    EventSerializer,
    FamilySerializer,
    ProofSerializer,
    SiteConfigurationSerializer,
)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Event.objects.filter(published=True)
    serializer_class = EventSerializer


class FamilyViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Challenge.objects.filter(published=True)
    serializer_class = ChallengeSerializer


class ProofViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    lookup_field = "uuid"
    queryset = Proof.objects.filter(published=True)
    serializer_class = ProofSerializer


class SiteConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
