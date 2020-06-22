from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):

    CITIES = (
            ('Cairo', 'Cairo'),
            ('Giza', 'Giza'),
            ('Alexandria', 'Alexandria'),
            ('Kafr El Sheikh', 'Kafr El Sheikh'),
            ('Ismailia', 'Ismailia'),
            ('Frontier governorates', 'Frontier governorates'),
            ('Gharbia', 'Gharbia'),
            ('Dakahlia', 'Dakahlia'),
            ('Monufia', 'Monufia'),
            ('Damietta', 'Damietta'),
            ('Suez', 'Suez'),
            ('Port Said', 'Port Said'),
            ('Qalyubia', 'Qalyubia'),
            ('Sharqia', 'Sharqia'),
            ('Beheira', 'Beheira'),
            ('Aswan', 'Aswan'),
            ('Qena', 'Qena'),
            ('Faiyum', 'Faiyum'),
            ('Minya', 'Minya'),
            ('Sohag', 'Sohag'),
            ('Asyut', 'Asyut'),
            ('Beni Suef', 'Beni Suef'),
            ('Luxor','Luxor')
        )

    GENDER =(('Male','Male'),('Female','Female'))
    phone_regex = RegexValidator(regex=r'^(01)[012][0-9]{8}',message="Sorry, Only Egyptian Phones are allowed...")

    first_name = models.CharField(max_length=25, null=False, blank=False)
    last_name = models.CharField(max_length=25, null=False, blank=False)
    username = models.CharField(max_length=25, unique=True, null=False, blank=False)
    email = models.EmailField(verbose_name="email", unique=True, null=False, blank=False)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=25, choices= GENDER, null=True, blank=False, default="Male")
    phone = models.CharField(validators=[phone_regex], unique=True, max_length=11, null=True, blank=True)
    city = models.CharField(max_length=30, choices=CITIES, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    
class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation')
    token = models.CharField(max_length=50, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"