from rest_framework import routers

from bdeapp.api.views import EventViewSet, ChallengeViewSet, FamilyViewSet

router = routers.DefaultRouter()
router.register("events", EventViewSet, basename="event")
router.register("challenges", ChallengeViewSet, basename="challenge")
router.register("families", FamilyViewSet, basename="family")

urlpatterns = router.urls
