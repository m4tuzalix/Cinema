from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdatePasswordForm, UserUpdateAvatar
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import Reservation, User_Seats, Movies
from django.core import serializers
import json
from datetime import datetime
from collections import OrderedDict

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'{user} has joined the society')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users_templates/register.html', {'form':form})

@login_required
def profile(request):
    user_info = User.objects.get(pk = request.user.id)
    dic = {}
    try:
        reserved = Reservation.objects.get(customer=user_info)
        for x in reserved.reservations.all():
            title = x.movie.title
            image = x.movie.image
            if title in dic:
                pass
            else:
                dic[title] = {"image":str(image)}
        context={
            "user_info":user_info,
            "reserved":json.dumps(dic)
    }
    except:
        context={
            "user_info":user_info,
            "reserved":json.dumps(dic)
    }
    return render(request, 'users_templates/profile.html', context)

@login_required
def reservations(request, movie):
    if request.user.is_authenticated:
        if request.method == "GET":
            user = User.objects.get(pk=request.user.pk)
            movie = Movies.objects.get(title=movie)
            user_reservations = User_Seats.objects.filter(movie=movie, user=user)
            reserved = {}
            for reservation in user_reservations:
                date = str(reservation.date)
                time = str(reservation.time)
                times = {time:[]}
                if not date in reserved:
                    reserved.update({date:{"times":{}}})
                for seat in reservation.seats.all():
                        user_seat = {seat.row:seat.number}
                        times[time].append(user_seat)
                reserved[date]["times"].update(times)
                
            sorted_dict = OrderedDict(sorted(reserved.items()))
            context = {
                "reserved":sorted_dict,
                "reserved_json":json.dumps(reserved, sort_keys=True),
                "movie":movie.title
            }
            return render(request, 'users_templates/reservations.html', context)
    else:
        return redirect("home")

@login_required
def password_change(request):
    if request.method == "POST":
        pass_change_form = UserUpdatePasswordForm(data=request.POST, user=request.user) 
        avatar_change_form = UserUpdateAvatar(data=request.POST, files=request.FILES, instance=request.user.profile)
        if pass_change_form.is_valid():
            pass_change_form.save()
            messages.success(request, 'The password has been changed, please relogin')
            return redirect('profile')
        if avatar_change_form.is_valid() and len(request.FILES) > 0:
            avatar_change_form.save()
            messages.success(request, 'The avatar has been changed')
            return redirect('profile')
        else:
            messages.warning(request, 'Please fill the gaps correctly')
            return redirect('password-change')
    else:
        pass_change_form = UserUpdatePasswordForm(user=request.user) 
        avatar_change_form = UserUpdateAvatar(instance=request.user.profile)
        context = {
            "pass":pass_change_form,
            "avatar":avatar_change_form
        }
        return render(request, 'users_templates/password_change.html', context)
