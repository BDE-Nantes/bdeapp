from rest_framework import mixins, viewsets

from bdeapp.challenges.models import Challenge, Proof
from bdeapp.events.models import Event
from bdeapp.families.models import Family

from .serializers import (
    ChallengeSerializer,
    EventSerializer,
    FamilySerializer,
    ProofSerializer,
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
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class ProofViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = []
    lookup_field = "uuid"
    queryset = Proof.objects.filter(published=True)
    serializer_class = ProofSerializer
