from django.shortcuts import render

def doctor_page(request):
    return render(request, 'doctorProfile.html')
