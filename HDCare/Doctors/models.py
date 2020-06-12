from django.db import models
from django.core.validators import RegexValidator , MaxValueValidator , MinValueValidator
from users.models import User


class Doctor(models.Model):
    image = models.ImageField(null=True, blank=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    phone_regex = RegexValidator(regex=r'^[\+2]?(01)(0|1|2|5)([0-9]{8})$', message="the format of phone number must be as : +20 111 111 1111")
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    specialization = models.CharField(max_length=60)
    bio = models.TextField()
    clinic_address = models.CharField(max_length=100)
    waiting_time = models.CharField(max_length=20, null=True)
    fees = models.IntegerField(null=True)


    def __str__(self):
        return f"{self.first_name}{self.last_name}"

class Doctor_Book(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , related_name='doctors')

    def __str__(self):
        return self.waiting_time

class UserBook(models.Model):
    doctor_book = models.ForeignKey(Doctor_Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('doctor_book','user')

class Comment(models.Model):
    context = models.TextField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('doctor','user')
    
    def __str__(self):
        return self.context

class Rate(models.Model):
    rate = models.IntegerField(validators=[MaxValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('doctor','user')


class Complain(models.Model):
    contain = models.TextField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.contain