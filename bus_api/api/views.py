from rest_framework import viewsets
from api.serializers import RouteSerializer
from api.models import Route


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
