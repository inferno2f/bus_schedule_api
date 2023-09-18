import csv

from api.models import Route, Stop, CalendarDates, Trip, StopTimes
from django.conf import settings
from django.core.management.base import BaseCommand

STATIC_FOLDER = settings.STATICFILES_DIRS[0]


def route_parser():
    with open(f"{STATIC_FOLDER}/routes.txt", "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for columns in csv_reader:
            route_id = int(columns[0])
            short_name = columns[2].strip('"')
            Route.objects.update_or_create(
                route_id=route_id,
                defaults={
                    "route_short_name": short_name,
                },
            )


def stop_parser():
    with open(f"{STATIC_FOLDER}/stops.txt", "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for columns in csv_reader:
            stop_id = int(columns[0])
            stop_code = int(columns[1])
            stop_name = columns[2].strip('"')
            stop_latitude = columns[4].strip('"')
            stop_longitude = columns[5].strip('"')
            zone_id = int(columns[6])
            Stop.objects.update_or_create(
                stop_id=stop_id,
                defaults={
                    "stop_code": stop_code,
                    "stop_name": stop_name,
                    "stop_latitude": stop_latitude,
                    "stop_longitude": stop_longitude,
                    "zone_id": zone_id,
                },
            )


def calendar_dates_parser():
    with open(f"{STATIC_FOLDER}/calendar_dates.txt", "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for columns in csv_reader:
            service_id = int(columns[0])
            date = columns[1]
            exception_type = int(columns[2])
            CalendarDates.objects.update_or_create(
                service_id=service_id,
                defaults={
                    "date": date,
                    "exception_type": exception_type,
                },
            )


def trip_parser():
    with open(f"{STATIC_FOLDER}/trips.txt", "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for columns in csv_reader:
            route_id = int(columns[0])
            service_id = int(columns[1])
            trip_id = int(columns[2])
            trip_headsign = columns[3].strip('"')
            direction_id = int(columns[4])
            route = Route.objects.get(route_id=route_id)
            service = CalendarDates.objects.get(service_id=service_id)
            Trip.objects.update_or_create(
                trip_id=trip_id,
                route=route,
                service=service,
                defaults={
                    "trip_headsign": trip_headsign,
                    "direction_id": direction_id,
                },
            )


def stop_times_parser():
    with open(f"{STATIC_FOLDER}/stop_times.txt", "r") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for columns in csv_reader:
            trip_id = int(columns[0])
            arrival_time = columns[1].strip('"')
            departure_time = columns[2].strip('"')
            stop_id = int(columns[3])
            trip = Trip.objects.get(trip_id=trip_id)
            stop = Stop.objects.get(stop_id=stop_id)
            StopTimes.objects.update_or_create(
                trip=trip,
                stop=stop,
                defaults={
                    "arrival_time": arrival_time,
                    "departure_time": departure_time,
                },
            )


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        route_parser()
        stop_parser()
        calendar_dates_parser()
        trip_parser()
        stop_times_parser()
