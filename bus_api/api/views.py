import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response, mixins
from api.serializers import (
    RouteSerializer,
    TripSerializer,
    CalendarSerializer,
    StopTimesSerializer,
)
from api.models import Route, Trip, CalendarDates, StopTimes


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
        service_id: {int}
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filterset_fields = ["service_id"]

    def list(self, request):
        service_ids = request.query_params.getlist("service_id")
        queryset = Trip.objects.distinct("route", "direction_id")
        if service_ids:
            queryset = queryset.filter(service_id__in=service_ids)

        serializer = TripSerializer(queryset, many=True)
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
        date = self.request.query_params.get("date")
        if date:
            return CalendarDates.objects.filter(date=date)
        else:
            current_date = datetime.date.today()
            formatted_date = current_date.strftime("%Y%m%d")
            return CalendarDates.objects.filter(date=formatted_date)


class RouteStopTimesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Returns a list of all arrival times of a route at a specified stop.

    Query parameters:
        stop_id: {int}
        service_id: {int} (can be multiple)
        route: {int}
    """
    serializer_class = StopTimesSerializer
    queryset = StopTimes.objects.none()

    def list(self, *args, **kwargs):
        stop_id = self.request.GET.get("stop_id")
        service_ids = self.request.GET.get("service_id")
        route = self.request.GET.get("route")

        if stop_id is not None and route is not None and service_ids:
            print(stop_id, service_ids, route)
            queryset = StopTimes.objects.filter(
                stop_id=stop_id,
                trip__service_id__in=service_ids,
                trip__route__route_short_name=route,
            ).order_by("arrival_time")
        else:
            queryset = StopTimes.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
