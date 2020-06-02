from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Hospital)
admin.site.register(Specializaiton)
admin.site.register(Book)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Complaint)
admin.site.register(User_Book)

