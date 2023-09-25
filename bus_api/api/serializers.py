from rest_framework import serializers
from api.models import Route, Trip, CalendarDates


class RouteSerializer(serializers.Serializer):
    route_id = serializers.IntegerField()
    bus_number = serializers.CharField(source="route_short_name")

    class Meta:
        model = Route
        fields = ("route_id", "route_short_name",)
        read_only_fields = "__all__"


class TripSerializer(serializers.Serializer):
    route = serializers.StringRelatedField(source='route.route_short_name')
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


class CalendarSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    date = serializers.CharField()
    exception_type = serializers.IntegerField()

    class Meta:
        model = CalendarDates
        fields = ("date", "service_id", "exception_type")
