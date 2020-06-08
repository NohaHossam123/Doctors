from django.urls import path
from .views import *


urlpatterns = [
    path('',doctors_page, name='doctors'),
    path('doctor/<id>', doctor_profile, name="doctor"),
]