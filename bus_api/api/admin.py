from django.contrib import admin
from api.models import Route, Stop, StopTimes, CalendarDates, Trip


class RouteAdmin(admin.ModelAdmin):
    search_fields = ("route_short_name",)


admin.site.register(Route, RouteAdmin)
admin.site.register(Stop)
admin.site.register(CalendarDates)
admin.site.register(Trip)
admin.site.register(StopTimes)
