from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    RouteStopsViewSet,
    RouteViewSet,
    TripViewSet,
    CalendarViewSet,
    RouteStopTimesViewSet,
)

app_name = "api"

router = SimpleRouter()
router.register(r"routes", RouteViewSet)
router.register(r"trips", TripViewSet)
router.register(r"calendar", CalendarViewSet)
router.register(r"route_stops", RouteStopsViewSet)
router.register(r"stop_times", RouteStopTimesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
