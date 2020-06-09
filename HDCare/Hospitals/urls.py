from django.urls import path, include
from .views import *


urlpatterns = [
    path('',hospitals , name='hospitals'),
    path('h/<id>',hospital , name='hospital'),
    path('books/<id>',hospital_books , name='hospital_books'),
    path('<id>/addReview',add_review,name="add_review"),
    path('<id>/removeReview',remove_review,name="remove_review"),

]
