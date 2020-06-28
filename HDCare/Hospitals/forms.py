from django import forms
from users.models import User
from .models import *


class AddHospital(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name','phone','image','location','about']

        widgets = {
            
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control' , 'rows' : 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class DateForm(forms.Form):
    start_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    end_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

class AddBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['start_time', 'end_time', 'fees','waiting_time','doctor','specializaiton']
        widgets = {
            'fees': forms.TextInput(attrs={'class': 'form-control'}),
            'waiting_time': forms.TextInput(attrs={'class': 'form-control'}),
            'doctor': forms.TextInput(attrs={'class': 'form-control'}),
            'specializaiton': forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2'}), 
        }
