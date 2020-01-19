from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    return render(request, 'users_templates/profile.html')