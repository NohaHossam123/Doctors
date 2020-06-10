from django.shortcuts import render, redirect
from users.models import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def doctors_page(request):
    doctors = Doctor.objects.all()
    rating = [1,2,3,4,5]
    context = {'doctors': doctors ,"rating": rating}
    return render(request, 'allDoctors.html', context)

def doctor_profile(request,id):
    doctor = Doctor.objects.get(id=id)
    rating = [1,2,3,4,5]
    comments = Comment.objects.order_by("-id").filter(doctor=id)
    context = {'doctor':doctor,'rating':rating , 'comments':comments}
    return render(request, 'doctorProfile.html', context)

@login_required
def add_comment(request,id):
    if request.method == 'POST':
        if request.POST.get('context') == '':
            messages.error(request, "Invalid comment,Comment can't be empty")
        else:
            user_id = request.user.id
            context= request.POST.get('context')
            Comment.objects.create(context= context,user_id = user_id, doctor_id = id)
    return redirect('doctor', id)

def remove_comment(request, id):
    comment = Comment.objects.get(id=id)
    doctor_id = comment.doctor.id
    comment.delete()
    return redirect('doctor', doctor_id)


