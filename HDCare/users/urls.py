from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', signin, name='signin'),
    path('profile/', profile, name='profile'),
    path('change-password/', password, name='password'),
    path('logout/', user_logout, name='logout'),
    path('', home, name='home'),
    # password reset
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),
    path('reset_password/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),
    # login with facebook
    path('oauth/', include('social_django.urls', namespace='social')),
    path('appointments/', appointments, name='appointments'),
    path('activate/<str:token>', activate_account, name="activate"),
    path('facebook', facebook, name="facebook"),
    path('twitter', twitter, name="twitter"),
]
