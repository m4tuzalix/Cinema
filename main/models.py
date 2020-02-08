from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth.models import User
from datetime import datetime, timedelta




AGE_CATEGORY = {
    ("0","All"),
    ("6","Kids"),
    ("16","Teenagers"),
    ("21","Adults")
}

MOVIE_CATEGORY = {
    ("H","Horror"),
    ("F","Fantasty"),
    ("ScI","Science-Fiction"),
    ("C","Comedy"),
    ("R","Romance"),
    ("T","Thriller"),
    ("D","Drama"),
}

Week_Days = {
    ("M", 'Monday'),
    ("T", 'Tuesday'),
    ("W", 'Wednesday'),
    ("Th", 'Thursday'),
    ("F", 'Friday'),
    ("S", 'Saturday'),
    ("Su", 'Sunday'),
}




class Movies(models.Model):
    title = models.CharField(max_length=100)
    age = models.CharField(choices=AGE_CATEGORY, max_length=2)
    kind = models.CharField(choices=MOVIE_CATEGORY, max_length=3)
    price = models.FloatField()
    description = models.TextField()
    cew = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to="movie_images")

    def __str__(self):
        return self.title


    def absolute(self):
        return reverse("movie", kwargs={
            'pk':self.pk
        })
    
    def order(self):
        return reverse("movie-order", kwargs={
            'pk':self.pk
        })

   
class Hours(models.Model):
    hours = models.TimeField(auto_now_add=False)

    def __str__(self):
        return f"{self.hours}"

class Dates(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)

    def __str__(self):
        return(f'{self.date}')

        

class Movie_dates(models.Model): #// signals appended - Creates this model straight after new Movie has been added
    main_movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    dates = models.ManyToManyField(Dates)
    time = models.ManyToManyField(Hours)
    unique_together = ('main_movie', 'date')

    def __str__(self):
        return(f'Available dates of {self.main_movie.title}')

class User_Seats(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    time = models.TimeField(auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.CharField(max_length = 1)
    number = models.IntegerField()
    ordered = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M"), blank=True, null=True) 
    

    def __str__(self):
        return f'Movie: {self.movie.title} Date: {self.date} Time: {self.time} Row: [{self.row}] Seat: [{self.number}]' 


class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    reservations = models.ManyToManyField(User_Seats)
    

    def __str__(self):
        return f'{self.customer} reservations'



