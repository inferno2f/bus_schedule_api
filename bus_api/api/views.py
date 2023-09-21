import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response, mixins
from api.serializers import RouteSerializer, DirectionSerializer, CalendarSerializer
from api.models import Route, Trip, CalendarDates


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def list(self, request):
        queryset = Route.objects.all()
        serializer = RouteSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Route.objects.all()
        route = get_object_or_404(queryset, pk=pk)
        serializer = RouteSerializer(route)
        return response.Response(serializer.data)


class TripViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Returns trips for any given day

    Query parameters:
        search_id: {int}
    """
    queryset = Trip.objects.all()
    serializer_class = DirectionSerializer
    filterset_fields = ["service_id"]

    def list(self, request):
        service_ids = request.query_params.getlist("service_id")
        queryset = Trip.objects.distinct("trip_headsign")
        if service_ids:
            queryset = queryset.filter(service_id__in=service_ids)

        serializer = DirectionSerializer(queryset, many=True)
        return response.Response(serializer.data)


class CalendarViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Returns a list of services active on a specified date.
    If no query parameters are passed returns today's services.

    Query parameters:
        date (YYYYMMDD): {str}
    """
    queryset = CalendarDates.objects.all()
    serializer_class = CalendarSerializer
    filterset_fields = ["date"]

    def get_queryset(self):
        # queryset = CalendarDates.objects.all()
        date = self.request.query_params.get('date')
        if date:
            return CalendarDates.objects.filter(date=date)
        else:
            current_date = datetime.date.today()
            formatted_date = current_date.strftime("%Y%m%d")
            return CalendarDates.objects.filter(date=formatted_date)
