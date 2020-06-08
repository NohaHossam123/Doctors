from django.shortcuts import render
from users.models import *
from .models import *

def doctors_page(request):
    doctors = Doctor.objects.all()
    rating = [1,2,3,4,5]
    context = {'doctors': doctors ,"rating": rating }
    return render(request, 'allDoctors.html', context)

def doctor_profile(request,id):
    doctor = Doctor.objects.get(id=id)
    rating = [1,2,3,4,5]
    context = {'doctor':doctor,'rating':rating}
    return render(request, 'doctorProfile.html', context)

