from django.urls import path, include
from .views import *


urlpatterns = [
    path('',hospitals , name='hospitals'),
    path('h/<id>',hospital , name='hospital'),
    path('books/<id>',hospital_books , name='hospital_books'),
    path('<id>/addReview',add_review,name="add_review"),
    path('<id>/removeReview',remove_review,name="remove_review"),
    path('<id>/editReview',edit_review,name="edit_review"),
    path('<id>/rate',rate_hospital,name="rate_hospital"),
    path('<id>/addComplaint',add_complaint,name="add_complaint"),
    path('book_hospital/<int:id>', book_redirect,name="hospital_book_redirect"),
    path('hospital', hospital_info, name="hospital"),
    path('addspecialization', add_specialize , name="addspecialization"),
    path('delete_specialize/<id>',delete_specialize , name="delete_specialize"),
    path('edit_specialize/<id>', edit_specialize , name="edit_specialize"),
    path('addbook',add_book, name="addbook"),
    path('delete_book<id>',delete_book, name="deletebook"),
    path('reservation', reservation_details, name="reservation_details"),
]
