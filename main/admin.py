from django.contrib import admin
from .models import Movies, Reservation, Movie_dates, Hours, User_Seats, Dates, Seats
from django.contrib.auth.models import User
from users.models import Profile



models = [Movies, Reservation, Profile, Movie_dates, Hours, User_Seats, Dates, Seats]

for model in models:
    admin.site.register(model)









