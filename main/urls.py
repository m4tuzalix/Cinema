from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("movies/", views.show_all_movies, name="movies"),
    path("movie/<int:pk>", views.show_single_movie.as_view(), name="movie"),
    path("movie-order/<int:pk>", views.order, name="movie-order"),
    path("make-order", views.make_order, name="make-order"),
    path("confirmation", views.confirmation, name="confirmation"),
    path("buy/<int:pk>", views.buy_seats, name="buy")
]