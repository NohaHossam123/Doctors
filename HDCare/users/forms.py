from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterationForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password*'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password*'}))

    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'gender', 'phone', 'city', 'birthdate']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'birthdate': 'Birth Date',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name*'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control' , 'placeholder': 'Last Name*'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email*'}),
            'birthdate': forms.SelectDateWidget(attrs={'class':'custom-select','style': 'width: 20%; display: inline-block;'}, years = range(2022, 1930, -1)),
            'gender': forms.RadioSelect(attrs={'class':'form-check-input mr-2'}),
            'city': forms.Select(attrs={'class': 'custom-select my-1 mr-sm-2'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),

        }


class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone','birthdate','city','gender','email','username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birthdate': forms.SelectDateWidget(attrs={'class':'custom-select','style': 'width: 20%; display: inline-block;'}, years = range(2022, 1930, -1)),
            'gender': forms.RadioSelect(attrs={'class':'form-check-input mr-2'}),
            'city': forms.Select(attrs={'class': 'custom-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),

        }

    
