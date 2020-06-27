from django.db import models
from django.core.validators import  MaxValueValidator , MinValueValidator
from django.utils import timezone
from datetime import date, datetime, timedelta
from users.models import User
from django.db.models import Avg
from smart_selects.db_fields import ChainedForeignKey 

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    about = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=11,unique=True, null=False, blank=False)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return str(self.name)

    @property
    def avg_rate(self):
        rate = Rating.objects.filter(hospital_id = self.id).aggregate(Avg('rate'))
        return rate['rate__avg']
    
    @property
    def count_rating(self):
        return self.rating_set.all().count()

class Specializaiton(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        unique_together = ('name','hospital')



class Book(models.Model):
    fees = models.FloatField(validators = [MinValueValidator(0.0)], null=False, blank=False)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    waiting_time = models.IntegerField(null=True)
    doctor = models.CharField(max_length=60,null=False,blank=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    specializaiton = ChainedForeignKey(
        Specializaiton, 
        chained_field='hospital', 
        chained_model_field='hospital',
        show_all=False,
        auto_choose=True,
        verbose_name='Specializaiton',
    )
    def __str__(self):
        return 'Book: %s - %s' % (self.hospital.name , self.specializaiton)
    

    def __repr__(self):
        return f"specialization={self.specializaiton.name}"

    @property
    def is_expired(self):
        return date.today() > self.end_time.date()


class Rating(models.Model):
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=False)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hospital','user')

    def __str__(self):
        return str(self.rate)



class Review(models.Model):
    context = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hospital','user')

    def __str__(self):
        return str(self.context)



class Complaint(models.Model):
    context = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hosptal = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class User_Book(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def is_old(self):
        return (timezone.now() - self.created_at) < timedelta(hours=24)

    class Meta:
        unique_together = ('book','user')
