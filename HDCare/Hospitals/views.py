from django.shortcuts import render, redirect
from .models import *
from users.views import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse



def hospitals(request):
    url_parameter = request.GET.get('q')
    print(url_parameter)
    if url_parameter:
        hospitals = Hospital.objects.filter(name__icontains=url_parameter)
    else:
        hospitals = Hospital.objects.all()

    context = {'hospitals': hospitals}

    if request.is_ajax():
        html = render_to_string(
            template_name="hospitals-partial.html", 
            context={'hospitals': hospitals}
        )

        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request,'all_hospitals.html', context)


def hospital(request, id):
    hospital = Hospital.objects.get(id=id)
    reviews = Review.objects.order_by("-id").filter(hospital=id)
    complains = Complaint.objects.all()
    context = {'hospital': hospital , 'reviews':reviews , "complains": complains}
    
    return render(request,'hospital.html', context)


def hospital_books(request, id):
    books = Book.objects.filter(specializaiton_id= id)
    context = {'books': books}

    return render(request,'books.html',context)

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

def edit_review(request, id):
    if request.method == 'POST':
        review = Review.objects.get(id=id)
        review.context = request.POST.get('context')
        if review.context == '':
            messages.error(request, "Invalid review,review can't be empty")
        else:  
            review.save()
    return redirect('hospital', review.hospital.id)

def add_complaint(request,id):
    if request.method == 'POST':
        if request.POST.get('context') == '':
            messages.error(request, "Invalid complain,Complain can't be empty")
        else:
            user_id = request.user.id
            context = request.POST.get('context')
            Complaint.objects.create(context= context, user_id = user_id, hosptal_id = id)
    return redirect('hospital', id)