from rest_framework import routers

from bdeapp.api.views import (
    ChallengeViewSet,
    EventViewSet,
    FamilyViewSet,
    ProofViewSet,
    SiteConfigurationViewSet,
)

app_name = "api"

router = routers.DefaultRouter()
router.register("events", EventViewSet, basename="event")
router.register("challenges", ChallengeViewSet, basename="challenge")
router.register("families", FamilyViewSet, basename="family")
router.register("proofs", ProofViewSet, basename="proof")
router.register(
    "siteconfiguration", SiteConfigurationViewSet, basename="siteconfiguration"
)

urlpatterns = router.urls
