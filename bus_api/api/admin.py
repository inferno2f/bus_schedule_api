from django.contrib import admin
from api.models import Route, Stop, StopTimes, CalendarDates, Trip

admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(CalendarDates)
admin.site.register(Trip)
admin.site.register(StopTimes)
