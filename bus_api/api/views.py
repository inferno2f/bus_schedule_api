import datetime

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, response, mixins

from api.models import Route, Trip, CalendarDates, StopTimes
from api.serializers import (
    RouteSerializer,
    RouteStopsSerializer,
    TripSerializer,
    CalendarSerializer,
    StopTimesSerializer,
)


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def list(self, request, **kwargs):
        queryset = Route.objects.all()
        serializer = RouteSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Route.objects.all()
        route = get_object_or_404(queryset, pk=pk)
        serializer = RouteSerializer(route)
        return response.Response(serializer.data)


class TripViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Returns a list of unique trips (inbound and outbound).
    Can be filtered bu query parameter `service_id`

    Query parameters:
        service_id: {int} (can be multiple)
    """

    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filterset_fields = ["service_id"]

    def list(self, request, **kwargs):
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


class RouteStopsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Returns a list of stops with names and ids for a specified route.

    Query params:
        route: {int}
        direction_id: {int} (binary)
    """
    serializer_class = RouteStopsSerializer
    queryset = StopTimes.objects.none()

    # Custom parameter fields for Swagger
    route = openapi.Parameter(
        "route", openapi.IN_QUERY, description="Route #", type=openapi.TYPE_NUMBER,
    )
    direction = openapi.Parameter(
        "direction_id", openapi.IN_QUERY, description="Direction ID", type=openapi.FORMAT_BINARY,
    )

    @swagger_auto_schema(manual_parameters=[route, direction])
    def list(self, *args, **kwargs):
        route = self.request.GET.get("route")
        direction_id = self.request.GET.get("direction_id")

        if (route and direction_id) is not None:
            queryset = (
                StopTimes.objects.filter(
                    trip__route__route_short_name=route,
                    trip__direction_id=direction_id,
                )
                .order_by("stop__stop_name")
                .distinct("stop__stop_name")
            )
        else:
            queryset = StopTimes.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class RouteStopTimesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Returns a list of all arrival times of a route at a specified stop.

    Query parameters:
        stop_id: {int}
        route: {int}
        direction_id: {int}
        service_id: {int} (can be multiple)
    """

    serializer_class = StopTimesSerializer
    queryset = StopTimes.objects.none()

    # Custom parameter fields for Swagger
    stop = openapi.Parameter(
        "stop_id", openapi.IN_QUERY, description="Stop ID", type=openapi.TYPE_NUMBER
    )
    service = openapi.Parameter(
        "service_id", openapi.IN_QUERY, description="Service ID(s)", type=openapi.TYPE_NUMBER
    )
    route = openapi.Parameter(
        "route", openapi.IN_QUERY, description="Route #", type=openapi.TYPE_NUMBER
    )
    direction = openapi.Parameter(
        "direction_id", openapi.IN_QUERY, description="Direction ID", type=openapi.FORMAT_BINARY
    )

    @swagger_auto_schema(manual_parameters=[stop, service, route, direction])
    def list(self, *args, **kwargs):
        stop_id = self.request.GET.get("stop_id")
        service_ids = self.request.GET.getlist("service_id")
        route = self.request.GET.get("route")
        direction_id = self.request.GET.get("direction_id")
        trip_id = self.request.GET.get("trip_id", None)

        if stop_id is not None and route is not None and service_ids:
            queryset = StopTimes.objects.filter(
                stop_id=stop_id,
                trip__service_id__in=service_ids,
                trip__route__route_short_name=route,
                trip__direction_id=direction_id,
            ).order_by("arrival_time").distinct("arrival_time")
        elif trip_id:
            queryset = StopTimes.objects.filter(trip__trip_id=trip_id).order_by(
                "arrival_time"
            )
        else:
            queryset = StopTimes.objects.none()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
