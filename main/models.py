from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth.models import User
from datetime import datetime




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

class Movies(models.Model):
    title = models.CharField(max_length=100)
    age = models.CharField(choices=AGE_CATEGORY, max_length=2)
    kind = models.CharField(choices=MOVIE_CATEGORY, max_length=3)
    price = models.FloatField()
    date = models.DateField()
    max_seats = models.IntegerField(default=100)
    description = models.TextField()

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

  
class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)
    number = models.IntegerField()
    ordered = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), blank=True, null=True) 

    def __str__(self):
        return f'{self.customer.username}:{self.movie.title}:{self.ordered}'

class Seat(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)
    number = models.IntegerField()
  
    def __str__(self):
        return f'{self.movie.title}:{self.row}:{self.number}'


