from django.shortcuts import render, redirect
from .models import *
from users.views import *
# Create your views here.

def hospitals(request):
    hospitals = Hospital.objects.all()
    context = {'hospitals': hospitals}
    
    return render(request,'all_hospitals.html', context)


def hospital(request, id):
    hospital = Hospital.objects.get(id=id)
    context = {'hospital': hospital}
    
    return render(request,'hospital.html', context)


def hospital_books(request, id):
    books = Book.objects.filter(specializaiton_id= id)
    context = {'books': books}

    return render(request,'books.html',context)