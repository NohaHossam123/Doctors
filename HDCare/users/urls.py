from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/',signup , name='signup'),
    path('login/',signin , name='signin'),
    path('profile/',profile , name='profile'),
    path('logout/',user_logout , name='logout'),
    path('', home , name='home'),
    path('appointments/', appointments , name='appointments'),


]