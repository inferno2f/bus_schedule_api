from django.db import models


class Route(models.Model):
    route_id = models.IntegerField(primary_key=True)
    route_short_name = models.CharField(max_length=255)


class Stop(models.Model):
    stop_id = models.IntegerField(primary_key=True)
    stop_code = models.IntegerField()
    stop_name = models.CharField(max_length=255)
    stop_latitude = models.FloatField()
    stop_longitude = models.FloatField()
    zone_id = models.IntegerField()


class CalendarDates(models.Model):
    service_id = models.IntegerField(primary_key=True)
    date = models.IntegerField()
    exception_type = models.IntegerField()


class Trip(models.Model):
    trip_id = models.IntegerField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service = models.ForeignKey(CalendarDates, on_delete=models.CASCADE)
    trip_headsign = models.CharField(max_length=255)
    direction_id = models.IntegerField()


class StopTimes(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
