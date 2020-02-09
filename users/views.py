from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main.models import Reservation
from django.core import serializers

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
    try:
        reserved = Reservation.objects.get(customer=user_info)
        res = []
        res.extend([x.movie for x in reserved.reservations.all()])
        context={
            "user_info":user_info,
            "reserved":serializers.serialize("json", set(res))
    }
    except:
        context={
            "user_info":user_info,
            "reserved":"You have no reservations"
    }
    return render(request, 'users_templates/profile.html', context)