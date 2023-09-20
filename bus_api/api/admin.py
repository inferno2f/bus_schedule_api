from django.contrib import admin
from api.models import Route, Stop, StopTimes, CalendarDates, Trip


class RouteAdmin(admin.ModelAdmin):
    search_fields = ("route_short_name",)


class StopTimesAdmin(admin.ModelAdmin):
    """Significantly improves performance of the admin panel"""
    raw_id_fields = ("trip", "stop",)


admin.site.register(Route, RouteAdmin)
admin.site.register(Stop)
admin.site.register(CalendarDates)
admin.site.register(Trip)
admin.site.register(StopTimes, StopTimesAdmin)
