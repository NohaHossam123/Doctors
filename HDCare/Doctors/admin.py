from django.contrib import admin
from .models import *

admin.site.register(Doctor)
admin.site.register(Doctor_Book)
admin.site.register(UserBook)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(Complain)

