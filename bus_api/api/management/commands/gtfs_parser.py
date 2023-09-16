import csv

from api.models import Route, Stop
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
                defaults={"route_short_name": short_name}
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
                }
            )


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        route_parser()
        stop_parser()
