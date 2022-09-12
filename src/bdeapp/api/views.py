
from rest_framework import viewsets

from bdeapp.events.models import Event
from bdeapp.challenges.models import Challenge
from bdeapp.families.models import Family

from .serializers import EventSerializer, ChallengeSerializer, FamilySerializer


class EventViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Event.objects.filter(published=True)
    serializer_class = EventSerializer


class FamilyViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    lookup_field = "uuid"
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
