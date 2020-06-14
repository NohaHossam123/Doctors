from django.urls import path
from .views import *


urlpatterns = [
    path('', doctors_page, name='doctors'),
    path('doctor/<id>', doctor_profile, name="doctor"),
    path('<id>/addComment', add_comment,name="add_comment"),
    path('<id>/removeComment', remove_comment,name="remove_comment"),
    path('<id>/editComment', edit_comment,name="edit_comment"),
    path('<id>/addComplain', add_complain,name="add_complain"),
    path('doctor/<id>/appointment', book_appointment,name="appointment"),
    path('doctor/<id>/book', book_redirect,name="book_redirect"),
    path('doctor/<id>/cancelAppointment', delete_appointment,name="delete_appointment"),
]