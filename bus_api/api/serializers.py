from rest_framework import serializers
from api.models import Route, Trip, CalendarDates, StopTimes


class RouteSerializer(serializers.ModelSerializer):
    route_id = serializers.IntegerField()
    bus_number = serializers.StringRelatedField(source="route_short_name")

    class Meta:
        model = Route
        fields = (
            "route_id",
            "bus_number",
        )
        read_only_fields = ["route_id", "bus_number"]


class CalendarSerializer(serializers.ModelSerializer):
    service_id = serializers.IntegerField()
    date = serializers.CharField()
    exception_type = serializers.IntegerField()

    class Meta:
        model = CalendarDates
        fields = ("date", "service_id", "exception_type")


class StopTimesSerializer(serializers.ModelSerializer):
    trip_id = serializers.IntegerField(source="trip.trip_id")
    stop_name = serializers.CharField(source="stop.stop_name")
    stop_id = serializers.IntegerField(source="stop.stop_id")

    class Meta:
        model = StopTimes
        fields = (
            "trip_id",
            "stop_name",
            "stop_id",
            "arrival_time",
        )


class RouteStopsSerializer(serializers.ModelSerializer):
    stop_id = serializers.IntegerField(source="stop.stop_id")
    stop_name = serializers.CharField(source="stop.stop_name")

    class Meta:
        model = StopTimes
        fields = (
            "stop_id",
            "stop_name",
        )


class TripSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField(source="route.route_short_name")
    trip_headsign = serializers.SerializerMethodField()
    direction_id = serializers.IntegerField()

    class Meta:
        model = Trip
        fields = ("route", "trip_headsign", "direction_id", "service_id",)

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
