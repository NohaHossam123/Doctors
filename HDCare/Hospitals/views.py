from django.shortcuts import render, redirect
from .models import *
from users.views import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import get_user
from datetime import date
from django.http import HttpResponseRedirect


def hospitals(request):

    specialize_hospital = Specializaiton.objects.all().values('name').distinct()
    url_parameter = request.GET.get('q')
    url_speciality = request.GET.get('s')

    if url_parameter:
        hospitals = Hospital.objects.filter(name__icontains=url_parameter)

    elif url_speciality:

        ids = Specializaiton.objects.filter(name__icontains = url_speciality).values_list("hospital") 
        hospitals = Hospital.objects.filter(id__in = ids)

    else:
        hospitals = Hospital.objects.all()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(hospitals, 6)
    
    try:
        hospitals = paginator.page(page)
    
    except PageNotAnInteger:
        hospitals = paginator.page(1)
    
    except EmptyPage:
        hospitals = paginator.page(paginator.num_pages)
    
    context = {'hospitals': hospitals , 'specialize_hospital':specialize_hospital}

    # ajax search
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
    rate = hospital.rating_set.all().values()
    try:
        user_rate = hospital.rating_set.get(user_id=request.user.id).rate
    except:
        user_rate = 0
    reviews = Review.objects.order_by("-id").filter(hospital=id)
    complains = Complaint.objects.all()
    context = {'hospital': hospital , 'reviews':reviews , "complains": complains , "user_rate":user_rate , "rate":rate}
    
    return render(request,'hospital.html', context)



def hospital_books(request, id):
    # hospital = Hospital.objects.get(id=id)
    user = get_user(request)
    all_books = user.user_book_set.all()
    all_books = [i.book_id for i in all_books]
    books = Book.objects.filter(specializaiton_id= id, end_time__date__gte = date.today())
    context = {'books': books, "all_books": all_books}

    return render(request,'books.html',context)



def book_redirect(request, id):
    user = get_user(request)
    book = Book.objects.get(id=id)
    User_Book.objects.create(user=user, book=book)
    messages.info(request,"your book has been placed susccessfully")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def delete_appointment(request, id):
    user = request.user
    appointment = User_Book.objects.get(user=user, book_id=id)
    appointment.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def add_review(request,id):
    try:
        if request.method == 'POST':
            if request.POST.get('context') == '':
                messages.error(request, "Invalid review,Review can't be empty")
            else:
                user_id = request.user.id
                context= request.POST.get('context')
                Review.objects.create(context= context,user_id = user_id, hospital_id = id)
    except:
        messages.error(request, "You have already commented to this doctor before!")
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
            messages.info(request,"we have received your complain")
    return redirect('hospital', id)



def rate_hospital(request,id):
    try:
        if request.method == 'POST':
            rate = request.POST.get('rate')
            Rating.objects.create(user_id=request.user.id, hospital_id=id, rate=rate) 
    except:
        rate = Rating.objects.get(user_id= request.user.id,hospital_id=id)
        rate.rate = request.POST.get('rate') 
        rate.save()
    return redirect('hospital', id)



def filter_hospitals(request):
    url_parameter = request.GET.get('q')
    if url_parameter:
        hospitals = Hospital.objects.filter(location__icontains=url_parameter)

    context = {'hospitals': hospitals}

    return render(request, 'all_hospitals.html', context)