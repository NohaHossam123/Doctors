from django.shortcuts import render, redirect
from .models import *
from users.views import *
# Create your views here.

def hospitals(request):
    hospitals = Hospital.objects.all()
    context = {'hospitals': hospitals}
    
    return render(request,'all_hospitals.html', context)
