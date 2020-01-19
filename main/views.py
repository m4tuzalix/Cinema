from django.shortcuts import render, get_object_or_404, redirect
from .models import Movies, Seat, Reservation
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import json
import simplejson



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
    template_name = "main_templates/movie.html"

def order(request, pk):
    movie = Movies.objects.get(pk=pk)
    row_name = ([chr(x) for x in range(65,65+20,1)])

    made_reservations = Reservation.objects.filter(movie=movie)
    reserved_seats = []
    for reserved in made_reservations:
        reserved_seats.append(reserved.row+":"+str(reserved.number))

    context = {
        "seats_range":row_name,
        "movie_id":movie.id,
        "movie_title":movie.title,
        "movie_price":movie.price,
        "reserved":reserved_seats
    }
    return render(request, "main_templates/order_seat.html", context)



@login_required
@csrf_exempt
def make_order(request):
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)
        request.session["user_info"] = data["array"]
        return HttpResponse(json.dumps(data["array"]))
    else:
        return redirect(request, 'home')


@login_required
def confirmation(request):
    if request.session.get("user_info"):
        user_info = request.session.pop("user_info")
        movie = Movies.objects.get(pk=user_info[0]["id"])
        seats = []
        for user in user_info:
            seats.append(str(user["row"])+":"+str(user["seat"]))

        context = {
            "movie":movie,
            "seats":seats
        }
        request.session["seats"] = seats
        return render(request, "main_templates/confirmation.html", context)
    else:
        return redirect("home")
    

@login_required
def buy_seats(request, pk):
    if request.method == "POST" and request.session.get("seats"):
        seats = request.session.pop("seats")
        for seat in seats:
            customer = User.objects.get(pk=request.user.id)
            movie = Movies.objects.get(pk=pk)
            new_reservation = Reservation.objects.create(customer=customer, movie=movie, row=seat[:1], number=int(seat[2:]))
            new_reservation.save()
        messages.success(request,"You have succesfully reserved the seats.")
        return redirect("home")
    return redirect("home")

