from rest_framework import serializers
from api.models import Route, Trip, CalendarDates, StopTimes
from api.fixtures.routes import route_headsigns


class RouteSerializer(serializers.ModelSerializer):
    route_id = serializers.IntegerField()
    bus_number = serializers.StringRelatedField(source="route_short_name")
    readable_headsign = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = (
            "route_id",
            "bus_number",
            "readable_headsign",
        )
        read_only_fields = ["route_id", "bus_number"]

    def get_readable_headsign(self, instance):
        if instance.route_short_name.lower() in route_headsigns:
            return route_headsigns[instance.route_short_name.lower()]


class CalendarSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField()
    date = serializers.CharField()
    exception_type = serializers.IntegerField()

    class Meta:
        model = CalendarDates
        fields = ("date", "service_id", "exception_type")


class StopTimesSerializer(serializers.ModelSerializer):
    trip_id = serializers.IntegerField(source="trip.trip_id")
    trip_headsign = serializers.SerializerMethodField()
    stop_name = serializers.CharField(source="stop.stop_name")
    stop_id = serializers.IntegerField(source="stop.stop_id")

    class Meta:
        model = StopTimes
        fields = (
            "trip_id",
            "trip_headsign",
            "stop_name",
            "stop_id",
            "arrival_time",
        )

    def get_trip_headsign(self, instance):
        fare = "-Exact Fare"
        parts = instance.trip.trip_headsign.split(" ")
        if len(parts) >= 2:
            return " ".join(parts[1:]).replace(fare, "")
        return instance.trip_headsign


class RouteStopsSerializer(serializers.ModelSerializer):
    stop_id = serializers.IntegerField(source="stop.stop_id")
    stop_name = serializers.CharField(source="stop.stop_name")
    stop_code = serializers.CharField(source="stop.stop_code")

    class Meta:
        model = StopTimes
        fields = (
            "stop_id",
            "stop_code",
            "stop_name",
            "stop_sequence",
        )


class TripSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField(source="route.route_short_name")
    trip_headsign = serializers.SerializerMethodField()
    direction_id = serializers.IntegerField()
    readable_headsign = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ("route", "trip_headsign", "direction_id", "service_id", "readable_headsign")

    def get_trip_headsign(self, instance):
        fare = "-Exact Fare"
        parts = instance.trip_headsign.split(" ")
        if len(parts) >= 2:
            return " ".join(parts[1:]).replace(fare, "")
        return instance.trip_headsign

    def get_stops(self, instance):
        stops_queryset = StopTimes.objects.filter(trip=instance)
        stop_serializer = RouteStopsSerializer(stops_queryset, many=True)
        return stop_serializer.data

    def get_readable_headsign(self, instance):
        if instance.route.route_short_name.lower() in route_headsigns:
            return route_headsigns[instance.route.route_short_name.lower()]
