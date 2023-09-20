from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import RouteViewSet, TripViewSet, CalendarViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r"routes", RouteViewSet)
router.register(r"trips", TripViewSet)
router.register(r"calendar", CalendarViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
