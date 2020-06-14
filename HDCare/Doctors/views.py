from django.shortcuts import render, redirect
from users.models import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
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


