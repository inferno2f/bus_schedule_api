from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import RouteViewSet

app_name = 'api'

router = SimpleRouter()
router.register(r"routes", RouteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
