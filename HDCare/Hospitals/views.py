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
from datetime import datetime
from django.http import HttpResponseRedirect
from .forms import *
from users.models import *
from django.db.models import Q


def hospitals(request):

    specialize_hospital = Specializaiton.objects.all().values('name').distinct()
    url_parameter = request.GET.get('q')
    url_speciality = request.GET.get('s')
    url_city = request.GET.get('c')
    
    if url_parameter:
        hospitals = Hospital.objects.filter(name__icontains=url_parameter)

    elif url_speciality:
        ids = Specializaiton.objects.filter(name__icontains = url_speciality).values_list("hospital") 
        hospitals = Hospital.objects.filter(id__in = ids)

    elif url_city:
        hospitals = Hospital.objects.filter(location__icontains=url_city)

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
            context={'hospitals': hospitals , 'specialize_hospital':specialize_hospital}
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


@login_required
def hospital_books(request, id):
    if request.user.is_authenticated:
    # hospital = Hospital.objects.get(id=id)
        user = get_user(request)
        all_books = user.user_book_set.all()
        all_books = [i.book_id for i in all_books]
        books = Book.objects.filter(specializaiton_id= id, end_time__date__gte = date.today())
    
    else:
        return redirect("signin")
    
    context = {'books': books, "all_books": all_books}

    return render(request,'books.html',context)



def book_redirect(request, id):
    user = get_user(request)
    book = Book.objects.get(id=id)
    User_Book.objects.create(user=user, book=book)
    messages.info(request,"Your book has been placed successfully")

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
        messages.error(request, "You have already commented to this hospital before!")
    return redirect('hospital', id)



def remove_review(request, id):
    review = Review.objects.get(id=id)
    hospital_id = review.hospital.id
    review.delete()
    return redirect('hospital', hospital_id)



def edit_review(request, id):
    if request.method == 'POST':
        review = Review.objects.get(id=id)
        review.context = request.POST.get('data')
        if review.context == '':
            messages.error(request, "Invalid review,review can't be empty")
        else:  
            review.save()
    return redirect('hospital', review.hospital.id)

def add_complaint(request,id):
    if request.method == 'POST':
        if request.POST.get('context') == '':
            messages.error(request, "Invalid complaint,Complaint cannot be empty")
        else:
            user_id = request.user.id
            context = request.POST.get('context')
            Complaint.objects.create(context= context, user_id = user_id, hosptal_id = id)
            messages.info(request,"We have received your complaint")
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
    
@login_required
def hospital_info(request):
    user = User.objects.get(id=request.user.id)
    form = AddHospital()
    hospital_info = None
    if Hospital.objects.filter(user_id = request.user.id).exists():
        hospital_info = Hospital.objects.get(user_id= request.user.id)
        if request.method == 'POST':
            form = AddHospital(request.POST , request.FILES, instance=hospital_info)
            if form.is_valid():
                hospital = form.save(commit = False)
                hospital.save()
                messages.success(request, "Your hospital information updated successfully")
                redirect('hospital')
        else:
            form = AddHospital(initial={
                'name': hospital_info.name.capitalize(),
                'phone': hospital_info.phone,
                'location': hospital_info.location,
                'about': hospital_info.about,
                'image': hospital_info.image,
                })
    else:
        if request.method == 'POST':
            form = AddHospital(request.POST , request.FILES)
            if form.is_valid():
                hospital = form.save(commit=False)
                hospital.user = request.user
                hospital.save()
                messages.success(request, "Your hospital information saved successfully")
                redirect('hospital')

    if request.user.is_hospital and user.is_confirmed ==2:
        return render(request, 'hospital_info.html', {'form': form , 'hospital_info' : hospital_info} )
    elif user.is_hospital and user.is_confirmed ==1:
        return redirect('waiting')
    elif user.is_hospital and user.is_confirmed == 0:
        return redirect('confirm')
    else:    
        return redirect('home')

@login_required
def add_specialize(request):
    user = User.objects.get(id=request.user.id)
    url_specialize = request.GET.get('q')
    try:
        if url_specialize:
            speciality = Specializaiton.objects.filter(name__icontains= url_specialize,hospital_id= request.user.hospital.id)
        else:
            speciality = Specializaiton.objects.filter(hospital_id= request.user.hospital.id)
    except:
        speciality = ''

    if request.method == 'POST':
        try: 
            name = request.POST.get('speialize')
            if name == '':
                messages.error(request,"Specialization name can't be empty")
            else:
                Specializaiton.objects.create(hospital_id=request.user.hospital.id,name=name)
        except:
            if speciality == '':
                messages.error(request, "You have to add your hospital info first")
            else:    
                messages.error(request, "This specialization is already exist")

    # ajax search
    if request.is_ajax():
        html = render_to_string(
            template_name="hos_specialize_partial.html",
            context = {'speciality':speciality} 
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    if user.is_hospital and user.is_confirmed ==2:
        return render(request, 'specialization.html',{'speciality': speciality})
    elif user.is_hospital and user.is_confirmed ==1:
        return redirect('waiting')
    elif user.is_hospital and user.is_confirmed == 0:
        return redirect('confirm')
    else:    
        return redirect('home')

@login_required
def delete_specialize(request,id):
    specialize = Specializaiton.objects.get(id=id)
    specialize.delete()
    return redirect('addspecialization')

@login_required
def edit_specialize(request,id):
    if request.method == 'POST':
        speciality = Specializaiton.objects.get(id=id)
        speciality.name = request.POST.get('data')
        if speciality.name == '':
            messages.error(request, "Name can't be empty!")
        else:  
            speciality.save()
    return redirect('addspecialization')

@login_required
def add_book(request):
    user = User.objects.get(id=request.user.id)
    url_parameter = request.GET.get('q')
    try:
        specializations = Specializaiton.objects.filter(hospital_id= request.user.hospital.id)

        if url_parameter:
            books = Book.objects.filter((Q(start_time__icontains=url_parameter) |Q(end_time__icontains=url_parameter)),hospital_id= request.user.hospital.id)
        else:
            books = Book.objects.filter(hospital_id= request.user.hospital.id, end_time__gte = date.today())
    except:
        books = ''
        specializations = ''
    
    if request.method == 'POST':
        try:
            start = request.POST.get('start')
            end = request.POST.get('end')
            fees = request.POST.get('fees')
            doctor = request.POST.get('doctor')
            waiting_time = request.POST.get('wating')
            speciality = request.POST.get('choose')
            specializaiton = Specializaiton.objects.get(id=speciality)
            start_time = datetime.strptime(start, "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(end, "%Y-%m-%d %H:%M")
            Date = datetime.now().strftime("%Y-%m-%d %H:%M")
            today = datetime.strptime(Date, "%Y-%m-%d %H:%M")
            if end_time < start_time:
                messages.error(request, "Error: End date should be after start date")
            elif start_time < today or end_time < today:
                messages.error(request, "Error: Start and end date cannot be before today")
            else: 
                Book.objects.create(hospital_id=request.user.hospital.id, start_time=start, end_time=end , fees=fees , doctor=doctor , waiting_time=waiting_time , specializaiton= specializaiton) 
                messages.success(request, "Book added successfully")
        except:
            messages.error(request, "Error: You have to add the hospital information first")
        return redirect('addbook')

    if request.is_ajax():
        html = render_to_string(
            template_name="hos_book_partial.html",
            context = {'books':books}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    if request.user.is_hospital and user.is_confirmed ==2:
        return render(request, 'addbook.html',{'books':books ,'specializations':specializations})
    elif user.is_hospital and user.is_confirmed ==1:
        return redirect('waiting')
    elif user.is_hospital and user.is_confirmed == 0:
        return redirect('confirm')
    else:    
        return redirect('home')


@login_required
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('addbook')

@login_required
def reservation_details(request):
    user = User.objects.get(id=request.user.id)
    url_parameter = request.GET.get('q')
    url_reservation = request.GET.get('r')
    try:
        ids = Book.objects.filter(hospital_id= request.user.hospital.id).values_list("id") 
        count = User_Book.objects.filter(book__in = ids, book__start_time__gte=date.today())
        if url_parameter:
            if url_parameter == 'up':
                books = count
        elif url_reservation:
            books = User_Book.objects.filter(book__in = ids , book__start_time__icontains=url_reservation)   
        else:
            books = User_Book.objects.filter(book__in = ids ).order_by('book__start_time')
    except:
        books = ''
        count = ''
    #ajax search
    if request.is_ajax():
        html = render_to_string(
            template_name="hos_res_partial.html",
            context = {'books':books}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    
    if request.user.is_hospital and user.is_confirmed ==2:
        return render(request, 'hospitalReservation.html',{'books': books, 'count': count})
    elif user.is_hospital and user.is_confirmed ==1:
        return redirect('waiting')
    elif user.is_hospital and user.is_confirmed == 0:
        return redirect('confirm')
    else:    
        return redirect('home')

    


