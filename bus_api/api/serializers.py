from rest_framework import serializers
from api.models import Route


class CharToIntegerField(serializers.Field):
    def to_representation(self, obj):
        try:
            return int(obj)
        except (TypeError, ValueError):
            return obj


class RouteSerializer(serializers.Serializer):
    route_id = serializers.IntegerField()
    bus_number = CharToIntegerField(source="route_short_name")

    class Meta:
        model = Route
        fields = ("route_id", "route_short_name",)
        read_only_fields = "__all__"
