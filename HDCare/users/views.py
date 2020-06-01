from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

#Signup
@unauthenticated_user
def signup(request):
    form = RegisterationForm()
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
        else:
            pass
    return render(request, 'register.html', {'form': form})


#login
@unauthenticated_user
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return HttpResponseRedirect(reverse('admin:index'))
            else:
                return redirect('profile')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html')

#home
def home(request):
    return render(request, 'home.html')

#profile
@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    form = EditUser(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': user.gender,
        'birthdate': user.birthdate,
        'city': user.city,
        'phone': user.phone,

        })
    return render(request,'personalPage.html', {'form': form})


#edit profile
@login_required
def edit_user(request):
    if request.method == 'POST':
        pass
    return "yes"




@login_required
def appointments(request):
    return render(request,'appointments.html')


#logout
def user_logout(request):
    logout(request)
    return redirect('home')