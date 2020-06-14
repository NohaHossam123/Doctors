from django.shortcuts import render, redirect
from users.models import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils import timezone
from datetime import date
from django.contrib.auth import get_user
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def doctors_page(request):
    rating = [1,2,3,4,5]

    # search:
    url_parameter = request.GET.get('q')
    print(url_parameter)
    if url_parameter:
        doctors = Doctor.objects.filter(Q(first_name__icontains=url_parameter) |Q(last_name__icontains=url_parameter))
    else:
        doctors = Doctor.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(doctors, 6)
    
    try:
        doctors = paginator.page(page)
    
    except PageNotAnInteger:
        doctors = paginator.page(1)
    
    except EmptyPage:
        doctors = paginator.page(paginator.num_pages)

    context = {'doctors': doctors ,"rating": rating}

    if request.is_ajax():
        html = render_to_string(

            template_name="doctors-partial.html", 
            context={'doctors': doctors ,"rating": rating}
        )

        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'allDoctors.html', context)



def doctor_profile(request,id):
    doctor = Doctor.objects.get(id=id)
    rating = [1,2,3,4,5]
    rate = doctor.rate_set.only("rate")
    try:
        user_rate = doctor.rate_set.get(user_id=request.user.id).rate
    except:
        user_rate = 0
    comments = Comment.objects.order_by("-id").filter(doctor=id)
    complains = Complain.objects.all()
    context = {'doctor':doctor,'rating':rating , 'comments':comments , 'complains':complains , "user_rate": user_rate}
    return render(request, 'doctorProfile.html', context)

def add_comment(request,id):
    try:
        if request.method == 'POST':
            if request.POST.get('context') == '':
                messages.error(request, "Invalid comment,Comment can't be empty")
            else:
                user_id = request.user.id
                context= request.POST.get('context')
                Comment.objects.create(context= context,user_id = user_id, doctor_id = id)
    except:
        messages.error(request , "You have already commented to this doctor before!")
    return redirect('doctor', id)

def remove_comment(request, id):
    comment = Comment.objects.get(id=id)
    doctor_id = comment.doctor.id
    comment.delete()
    return redirect('doctor', doctor_id)

def edit_comment(request, id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=id)
        comment.context = request.POST.get('context')
        if comment.context == '':
            messages.error(request, "Invalid complain,Complain can't be empty")
        else:  
            comment.save()
    return redirect('doctor', comment.doctor.id)

def add_complain(request,id):
    if request.method == 'POST':
        if request.POST.get('contain') == '':
            messages.error(request, "Invalid complain,Complain can't be empty")
        else:
            user_id = request.user.id
            contain = request.POST.get('contain')
            Complain.objects.create(contain= contain,user_id = user_id, doctor_id = id)
            messages.info(request,"we have received your complain")
    return redirect('doctor', id)

def book_appointment(request,id):
    doctor = Doctor.objects.get(id=id)
    user = get_user(request)
    books = user.userbook_set.all()
    books = [i.doctor_book_id for i in books]
    book_info = Doctor_Book.objects.filter(
        doctor_id=id, end_time__date__gte = date.today()
    )
    context = {'book_info': book_info, "books": books}

    return render(request, 'book.html', context)

def book_redirect(request,id):
    user = request.user
    UserBook.objects.create(user=user, doctor_book_id=id)
    book_id = Doctor_Book.objects.get(id=id)
    messages.info(request,"your book has been placed susccessfully")

    return redirect('appointment', book_id.doctor_id)

def delete_appointment(request, id):
    user = request.user
    appointment = UserBook.objects.get(user=user, doctor_book_id=id)
    appointment.delete()
    book_id = Doctor_Book.objects.get(id=id)
    
    return redirect('appointment', book_id.doctor_id)
def rate_doctor(request,id):
    try:
        if request.method == 'POST':
            rate = int(request.POST.get('rate'))
            Rate.objects.create(user_id=request.user.id, doctor_id=id, rate=rate) 
    except:
        rate = Rate.objects.get(user_id= request.user.id,doctor_id=id)
        rate.rate = int(request.POST.get('rate')) 
        rate.save()
    return redirect('doctor', id)


