from django.urls import path
from .views import *


urlpatterns = [
    path('', doctors_page, name='doctors'),
    path('doctor/<id>', doctor_profile, name="doctor"),
    path('<id>/addComment', add_comment,name="add_comment"),
    path('<id>/removeComment', remove_comment,name="remove_comment"),
    path('<id>/editComment', edit_comment,name="edit_comment"),
    path('<id>/rate',rate_doctor,name="rate_doctor"),
    path('<id>/addComplain', add_complain,name="add_complain"),
    path('doctor/<int:id>/appointment', book_appointment,name="appointment"),
    path('doctor/<int:id>/book', book_redirect,name="book_redirect"),
    path('doctor/<int:id>/cancelAppointment', delete_appointment,name="delete_appointment"),
    path('<slug:token>/activate', copoun_activation,name="activate_copoun"),
    path('clinic',clinic_info, name="clinic"),
    path('addbook',add_book, name="add_book"),
    path('deletebook/<id>', delete_book, name="delete_book"),
    path('reservation', reservation_details, name="reservation_details"),




    # path('filterd', filter_doctors, name="filterbytitle"),
]