from django.shortcuts import render, redirect
from users.models import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse

def doctors_page(request):
    rating = [1,2,3,4,5]

    # search:
    url_parameter = request.GET.get('q')
    print(url_parameter)
    if url_parameter:
        doctors = Doctor.objects.filter(Q(first_name__icontains=url_parameter) |Q(last_name__icontains=url_parameter))
    else:
        doctors = Doctor.objects.all()

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
    comments = Comment.objects.order_by("-id").filter(doctor=id)
    complains = Complain.objects.order_by("-id").filter(doctor=id)
    context = {'doctor':doctor,'rating':rating , 'comments':comments , 'complains':complains}
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

def add_complain(request,id):
    if request.method == 'POST':
        if request.POST.get('contain') == '':
            messages.error(request, "Invalid complain,Complain can't be empty")
        else:
            user_id = request.user.id
            contain = request.POST.get('contain')
            Complain.objects.create(contain= contain,user_id = user_id, doctor_id = id)
    return redirect('doctor', id)



