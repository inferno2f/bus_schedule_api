from django.core.management.base import BaseCommand
from api.models import Route
from django.conf import settings


STATIC_FOLDER = settings.STATICFILES_DIRS[0]


def route_parser():
    with open(f"{STATIC_FOLDER}/routes.txt", "r") as f:
        next(f)
        for line in f:
            columns = line.strip().split(",")
            route_id = int(columns[0])
            short_name = columns[2].strip('"')
            route, created = Route.objects.get_or_create(route_id=route_id)
            if not created:
                route.short_name = short_name
                route.save()
            route.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        route_parser()
