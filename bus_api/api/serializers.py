from rest_framework import serializers
from api.models import Route, Trip, CalendarDates, StopTimes


class RouteSerializer(serializers.ModelSerializer):
    route_id = serializers.IntegerField()
    bus_number = serializers.CharField(source="route_short_name")

    class Meta:
        model = Route
        fields = (
            "route_id",
            "route_short_name",
        )
        read_only_fields = "__all__"


class TripSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField(source="route")
    trip_headsign = serializers.SerializerMethodField()
    direction_id = serializers.IntegerField()

    def get_trip_headsign(self, instance):
        parts = instance.trip_headsign.split(" ")
        if len(parts) >= 2:
            return " ".join(parts[1:])
        return instance.trip_headsign

    class Meta:
        model = Trip
        fields = ("route", "trip_headsign", "direction_id")


class CalendarSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField()
    date = serializers.CharField()
    exception_type = serializers.IntegerField()

    class Meta:
        model = CalendarDates
        fields = ("date", "service_id", "exception_type")


class StopTimesSerializer(serializers.ModelSerializer):
    trip = serializers.CharField(source="trip.trip_headsign")
    stop_name = serializers.CharField(source="stop.stop_name")
    stop_id = serializers.CharField(source="stop.stop_id")

    class Meta:
        model = StopTimes
        fields = (
            "trip",
            "stop_name",
            "stop_id",
            "arrival_time",
        )
