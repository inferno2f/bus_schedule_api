from rest_framework import serializers
from api.models import Route, Trip, CalendarDates


class CharToIntegerField(serializers.Field):
    def to_representation(self, obj):
        try:
            return int(obj)
        except (TypeError, ValueError):
            return obj


class RouteSerializer(serializers.Serializer):
    route_id = serializers.IntegerField()
    bus_number = serializers.CharField(source="route_short_name")

    class Meta:
        model = Route
        fields = ("route_id", "route_short_name",)
        read_only_fields = "__all__"


class DirectionSerializer(serializers.Serializer):
    # route = serializers.StringRelatedField(many=True)
    trip_headsign = serializers.CharField()
    # direction_id = serializers.IntegerField()

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
