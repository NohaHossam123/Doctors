from django.urls import path
from .views import *


urlpatterns = [
    path('doctorProfile/',doctor_page, name='doctorProfile'),

]