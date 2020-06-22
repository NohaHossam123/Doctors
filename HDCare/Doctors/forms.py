from django import forms
from users.models import User
from .models import *


class AddDoctor(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name','last_name','phone','image','clinic_address','specialization','bio','waiting_time','fees']

        widgets = {
            
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'clinic_address': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control' , 'rows' : 3}),
            'waiting_time': forms.TextInput(attrs={'class': 'form-control'}),
            'fees': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),

        }


