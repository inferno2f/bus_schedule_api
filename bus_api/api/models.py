from django.db import models


class Route(models.Model):
    route_id = models.IntegerField(primary_key=True)
    route_short_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Route #: {self.route_short_name}"


class Stop(models.Model):
    stop_id = models.IntegerField(primary_key=True)
    stop_code = models.IntegerField(null=True)
    stop_name = models.CharField(max_length=255)
    stop_latitude = models.CharField(max_length=36)
    stop_longitude = models.CharField(max_length=36)
    zone_id = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.stop_code}: {self.stop_name}"


class CalendarDates(models.Model):
    service_id = models.IntegerField()
    date = models.CharField(max_length=50)
    exception_type = models.IntegerField()

    class Meta:
        verbose_name = "Calendar dates"
        verbose_name_plural = "Calendar dates"

    def __str__(self):
        year = self.date[0:4]
        month = self.date[4:6]
        day = self.date[6:]
        return f"{year}/{month}/{day}"


class Trip(models.Model):
    trip_id = models.IntegerField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    service_id = models.IntegerField()
    trip_headsign = models.CharField(max_length=255)
    direction_id = models.IntegerField()

    def __str__(self):
        return f"{self.trip_headsign}"


class StopTimes(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    arrival_time = models.CharField(max_length=255)
    departure_time = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Stop times"
        verbose_name_plural = "Stop times"

    def __str__(self) -> str:
        return f"{self.stop.stop_name}: {self.arrival_time}"
