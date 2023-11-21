import csv
import os
from itertools import islice

from api.models import Route, Stop, CalendarDates, Trip, StopTimes
from django.core.management.base import BaseCommand
from django.db import transaction

DATA_FOLDER = os.path.join(BASE_DIR, "data")


def batch_iterator(iterable, batch_size):
    it = iter(iterable)
    while True:
        batch = list(islice(it, batch_size))
        if not batch:
            break
        yield batch


def route_parser():
    with open(f"{DATA_FOLDER}/routes.txt", "r") as f:
        Route.objects.all().delete()
        csv_reader = csv.reader(f)
        next(csv_reader)
        batch_size = 100
        for batch in batch_iterator(csv_reader, batch_size):
            bulk_insert_list = []
            for columns in batch:
                route_id = int(columns[0])
                short_name = columns[2].strip('"')
                bulk_insert_list.append(
                    Route(
                        route_id=route_id,
                        route_short_name=short_name,
                    )
                )
            Route.objects.bulk_create(bulk_insert_list)


@transaction.atomic
def stop_parser():
    with open(f"{DATA_FOLDER}/stops.txt", "r") as f:
        Stop.objects.all().delete()
        csv_reader = csv.reader(f)
        next(csv_reader)
        batch_size = 500
        for batch in batch_iterator(csv_reader, batch_size):
            bulk_insert_list = []
            for columns in batch:
                stop_id = int(columns[0])
                stop_code = int(columns[1])
                stop_name = columns[2].strip('"')
                stop_latitude = columns[4].strip('"')
                stop_longitude = columns[5].strip('"')
                zone_id = int(columns[6])
                bulk_insert_list.append(
                    Stop(
                        stop_id=stop_id,
                        stop_code=stop_code,
                        stop_name=stop_name,
                        stop_latitude=stop_latitude,
                        stop_longitude=stop_longitude,
                        zone_id=zone_id,
                    )
                )
            Stop.objects.bulk_create(bulk_insert_list)


@transaction.atomic
def calendar_dates_parser():
    with open(f"{DATA_FOLDER}/calendar_dates.txt", "r") as f:
        CalendarDates.objects.all().delete()
        csv_reader = csv.reader(f)
        next(csv_reader)
        batch_size = 500
        for batch in batch_iterator(csv_reader, batch_size):
            bulk_insert_list = []
            for columns in batch:
                service_id = int(columns[0])
                date = columns[1]
                exception_type = int(columns[2])
                bulk_insert_list.append(
                    CalendarDates(
                        service_id=service_id,
                        date=date,
                        exception_type=exception_type,
                    )
                )
            CalendarDates.objects.bulk_create(bulk_insert_list)


@transaction.atomic
def trip_parser():
    with open(f"{DATA_FOLDER}/trips.txt", "r") as f:
        Trip.objects.all().delete()
        csv_reader = csv.reader(f)
        next(csv_reader)
        batch_size = 500
        for batch in batch_iterator(csv_reader, batch_size):
            bulk_insert_list = []
            for columns in batch:
                route_id = int(columns[0])
                service_id = int(columns[1])
                trip_id = int(columns[2])
                trip_headsign = columns[3].strip('"')
                direction_id = int(columns[4])
                route = Route.objects.get(route_id=route_id)
                bulk_insert_list.append(
                    Trip(
                        trip_id=trip_id,
                        route=route,
                        service_id=service_id,
                        trip_headsign=trip_headsign,
                        direction_id=direction_id,
                    )
                )
            Trip.objects.bulk_create(bulk_insert_list)


@transaction.atomic
def stop_times_parser():
    with open(f"{DATA_FOLDER}/stop_times.txt", "r") as f:
        StopTimes.objects.all().delete()
        csv_reader = csv.reader(f)
        next(csv_reader)
        batch_size = 500
        for batch in batch_iterator(csv_reader, batch_size):
            bulk_insert_list = []
            for columns in batch:
                trip_id = int(columns[0])
                arrival_time = columns[1].strip('"')
                departure_time = columns[2].strip('"')
                stop_id = int(columns[3])
                trip = Trip.objects.get(trip_id=trip_id)
                stop = Stop.objects.get(stop_id=stop_id)
                bulk_insert_list.append(
                    StopTimes(
                        trip=trip,
                        stop=stop,
                        arrival_time=arrival_time,
                        departure_time=departure_time,
                    )
                )
            StopTimes.objects.bulk_create(bulk_insert_list)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        route_parser()
        stop_parser()
        calendar_dates_parser()
        trip_parser()
        stop_times_parser()
