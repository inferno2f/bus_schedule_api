from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response
from api.serializers import RouteSerializer
from api.models import Route


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def list(self, request):
        queryset = Route.objects.all()
        serializer = RouteSerializer()(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Route.objects.all()
        route = get_object_or_404(queryset, pk=pk)
        serializer = RouteSerializer(route)
        return response.Response(serializer.data)
