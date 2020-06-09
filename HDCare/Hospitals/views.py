from django.shortcuts import render, redirect
from .models import *
from users.views import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def hospitals(request):
    hospitals = Hospital.objects.all()
    context = {'hospitals': hospitals}
    
    return render(request,'all_hospitals.html', context)


def hospital(request, id):
    hospital = Hospital.objects.get(id=id)
    reviews = Review.objects.order_by("-id")
    context = {'hospital': hospital , 'reviews':reviews}
    
    return render(request,'hospital.html', context)


def hospital_books(request, id):
    books = Book.objects.filter(specializaiton_id= id)
    context = {'books': books}

    return render(request,'books.html',context)

@login_required
def add_review(request,id):
    if request.method == 'POST':
        if request.POST.get('context') == '':
            messages.error(request, "Invalid review,Review can't be empty")
        else:
            user_id = request.user.id
            context= request.POST.get('context')
            Review.objects.create(context= context,user_id = user_id, hospital_id = id)
    return redirect('hospital', id)

def remove_review(request, id):
    review = Review.objects.get(id=id)
    hospital_id = review.hospital.id
    review.delete()
    return redirect('hospital', hospital_id)