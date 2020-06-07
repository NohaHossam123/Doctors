from django.urls import path
from .views import *


urlpatterns = [
    path('allDoctors/',doctors_page, name='allDoctors'),

]