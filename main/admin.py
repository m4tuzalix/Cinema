from django.contrib import admin
from .models import Movies, Seat, Reservation


admin.site.register(Movies)
admin.site.register(Seat)
admin.site.register(Reservation)
