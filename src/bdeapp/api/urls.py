from rest_framework import routers

from bdeapp.api.views import ChallengeViewSet, EventViewSet, FamilyViewSet, ProofViewSet

router = routers.DefaultRouter()
router.register("events", EventViewSet, basename="event")
router.register("challenges", ChallengeViewSet, basename="challenge")
router.register("families", FamilyViewSet, basename="family")
router.register("proofs", ProofViewSet, basename="proof")

urlpatterns = router.urls
