from django.shortcuts import render, redirect
from .models import *
from users.views import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def hospitals(request):
    url_parameter = request.GET.get('q')
    print(url_parameter)
    if url_parameter:
        hospitals = Hospital.objects.filter(name__icontains=url_parameter)
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
    
    context = {'hospitals': hospitals}

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
    books = Book.objects.filter(specializaiton_id= id)
    context = {'books': books}

    return render(request,'books.html',context)


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


def book_appointment(request,id):
    if request.user.is_authenticated:
        doctor = Doctor.objects.get(id=id)
        user = get_user(request)
        books = user.userbook_set.all()
        books = [i.doctor_book_id for i in books]
        books_count = len(books)
        book_info = Doctor_Book.objects.filter(
            doctor_id=id, end_time__date__gte = date.today()
        )
        copoun = user.copoun.last()
        token = None
        if copoun:
            token = copoun.token
        context = {'book_info': book_info, "books": books, 'books_count': books_count, 'token': token}

        return render(request, 'book.html', context)
    else:
        return redirect('signin')

def book_redirect(request,id):
    user = get_user(request)
    obj = UserBook.objects.filter(user=user)
    if not obj:
        token = get_random_string(length=6)
        Copoun.objects.create(token=token, user=user)
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