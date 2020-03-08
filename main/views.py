from django.shortcuts import render, get_object_or_404, redirect
from .models import Movies, Reservation, User_Seats, Movie_dates, Seats
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core import serializers
import json
import simplejson
from datetime import datetime, timedelta, time
import requests
from bs4 import BeautifulSoup




def home(request):
    return render(request, "main_templates/main.html")

def show_all_movies(request):
    MOVIE_CATEGORY_COLORS = {
    ("H","danger"),
    ("F","primary"),
    ("ScI","secondary"),
    ("C","warning"),
    ("R","success"),
    ("T","dark"),
    ("D","info"),
}
    color_final = []
    for movie in Movies.objects.all():
        for color in MOVIE_CATEGORY_COLORS:
            if movie.kind in color:
                color_final.append(color[1])


    context = {
        "Movies_Colors": zip(Movies.objects.all(), color_final),
    }
    return render(request, "main_templates/movies.html", context)

class show_single_movie(DetailView):
    model = Movies
    query_pk_and_slug = True
    template_name = "main_templates/movie.html"
    def get_context_data(self, **kwargs):
        context = super(show_single_movie, self).get_context_data(**kwargs)
        movie = Movies.objects.get(pk=self.kwargs["pk"])
        all_dates = Movie_dates.objects.get(main_movie=movie)
        dic = {}
        for d in all_dates.dates.all():
            times_array = []
            for t in all_dates.time.all():
                times_array.append(str(t))
            dic[str(d.date)] = times_array
        context["dates"] = dic

        movie_details = requests.get(f"http://www.omdbapi.com/?t={movie.title}&apikey=23529a34").json() #// movie api to gather details about movie
        context["details"] = json.dumps(movie_details)

        actors_pics = {}
        actors = movie_details["Actors"].split(",")
        for actor in actors: #// to retrieve links to imdb where user can check the particular actor + to retireve photo links
            split_name = actor.strip().split(" ")
            url = requests.get(f"https://www.imdb.com/find?q={split_name[0]}+{split_name[1]}&ref_=nv_sr_sm").text
            soup = BeautifulSoup(url, "lxml")
            image = soup.find("td", {"class":"primary_photo"}).find("img")["src"]
            link = soup.find("td", {"class":"primary_photo"}).find("a")["href"]
            full_link = "https://www.imdb.com"+link+"?ref_=fn_al_nm_1"
            actors_pics[actor.strip()] = [image, full_link] #// named JSON with array as the content
       
        context["actor_pics"] = json.dumps(actors_pics)
        return context

@login_required
@csrf_exempt
def date_choose(request):
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)
        request.session["user_choice"] = data["container"]
        return HttpResponse(json.dumps(data["container"]))
    else:
        return redirect(request, 'home')

@login_required
def order(request, pk):
    if request.session.get("user_choice"):
        user_choice = request.session.pop("user_choice")
        movie_date = user_choice["date"]
        movie_hour = user_choice["hour"]
        movie = Movies.objects.get(pk=pk)
        row_name = ([chr(x) for x in range(65,65+20,1)]) #// 65 is A so 20 letters for row naming

        all_seats = Seats.objects.filter(movie=movie, date=movie_date, time=movie_hour)
        reserved_seats = []
        for reserved in all_seats:
            try:
                still_reserved = Reservation.objects.get(customer=reserved.user) #// if reservation has been deleted, delete the seats
                reserved_seats.append(reserved.row+":"+str(reserved.number))
            except:
                reserved.delete()
        
        context = {
            "seats_range":row_name,
            "movie_id":movie.id,
            "movie_title":movie.title,
            "movie_price":movie.price,
            "reserved":reserved_seats,
            "date": movie_date,
            "hour": movie_hour
            
        }
        request.session["user_choice"] = user_choice
        return render(request, "main_templates/order_seat.html", context)
    return redirect("home")


@login_required
@csrf_exempt
def make_order(request):
    if request.session.get("user_choice"):
        if request.method == "POST" and request.is_ajax():
            data = json.loads(request.body)
            request.session["user_info"] = data["array"]
            request.session["user_choice"] = request.session.pop("user_choice")
            return HttpResponse(json.dumps(data["array"]))
    else:
        return redirect(request, 'home')


@login_required
def confirmation(request):
    if request.session.get("user_info") and request.session.get("user_choice"):
        user_info = request.session.pop("user_info")
        user_choice = request.session.pop("user_choice")
        movie = Movies.objects.get(pk=user_info[0]["id"])
        customer = User.objects.get(pk=request.user.pk)
        seats = []
        for user in user_info:
            seats.append(str(user["row"])+":"+str(user["seat"]))
        context = {
            "movie":movie,
            "seats":seats
        }
        request.session["seats"] = seats
        request.session["user_choice"] = user_choice
        return render(request, "main_templates/confirmation.html", context)
    else:
        return redirect("home")
    

@login_required
def buy_seats(request, pk):
    if request.method == "POST" and request.session.get("seats") and request.session.get("user_choice"):
        seats = request.session.pop("seats")
        user_choice = request.session.pop("user_choice")
        movie = Movies.objects.get(pk=pk)
        customer = User.objects.get(pk=request.user.id)
        for s in seats:
            new_seat_create = Seats.objects.create(
                movie=movie, 
                user=customer, 
                row=s[:1], number=int(s[2:]), 
                date=user_choice["date"], 
                time=user_choice["hour"])
            new_seat_create.save()

            new_seat_get = Seats.objects.get(
                movie=movie, user=customer, 
                row=s[:1], number=int(s[2:]), 
                date=user_choice["date"], 
                time=user_choice["hour"])

            user_seats, created = User_Seats.objects.get_or_create(
                movie=movie, 
                user=customer, 
                date=user_choice["date"], 
                time=user_choice["hour"])
            user_seats.seats.add(new_seat_get)

            user_reserved_seats = User_Seats.objects.get(
                movie=movie, 
                user=customer, 
                date=user_choice["date"], 
                time=user_choice["hour"])
            reservation, created = Reservation.objects.get_or_create(
                customer=customer, 
                )
           
            reservation.reservations.add(user_reserved_seats)
        messages.success(request,"You have succesfully reserved the seats.")
        return redirect("home")
    return redirect("home")

