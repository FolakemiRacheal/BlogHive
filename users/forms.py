from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserSignupForm(UserCreationForm):
    email = forms.EmailField()
    phonenumber = forms.CharField()

    class Meta:
        model = User
        fields = ['username','email','phonenumber', 'password1','password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    phonenumber = forms.CharField()

    class Meta:
        model = User
        fields = ['username','email','phonenumber'] 


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields = ['image']