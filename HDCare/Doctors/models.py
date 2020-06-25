from django.db import models
from django.core.validators import RegexValidator , MaxValueValidator , MinValueValidator
from users.models import User
import datetime
from django.utils import timezone
from users.models import User
from django.db.models import Avg


class Doctor(models.Model):
    image = models.ImageField(null=True, blank=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    phone_regex = RegexValidator(regex=r'^[\+2]?(01)(0|1|2|5)([0-9]{8})$', message="the format of phone number must be as : +20 111 111 1111")
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    specialization = models.CharField(max_length=255)
    bio = models.TextField()
    clinic_address = models.CharField(max_length=255)
    waiting_time = models.CharField(max_length=20, null=True)
    fees = models.IntegerField(null=True, validators = [MinValueValidator(0)])
    user = models.OneToOneField(User, on_delete=models.CASCADE , blank=True, null=True, limit_choices_to={'is_doctor':True})

    def __str__(self):
        return f"{self.first_name}{self.last_name}"

    @property
    def avg_rating(self):
        rate = Rate.objects.filter(doctor_id = self.id).aggregate(Avg('rate'))
        return rate['rate__avg']

    @property
    def count_rating(self):
        return self.rate_set.all().count()

    @property
    def new_fees(self):
        return self.fees * 2
        

class Doctor_Book(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , related_name='doctors')

    @property
    def is_expired(self):
        return datetime.date.today() > self.end_time.date()
    
    

class UserBook(models.Model):
    doctor_book = models.ForeignKey(Doctor_Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_urgent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_cancelable(self):
        return (timezone.now() - self.created_at) < datetime.timedelta(hours=24)

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

class Copoun(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='copoun')
    token = models.CharField(max_length=10, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"