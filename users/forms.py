from django import forms
from django.contrib.auth.models import User
from CustomUser.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField

    class Meta:
        model = CustomUser
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class AddFundsForm(forms.Form):
      amount = forms.IntegerField(min_value=1, max_value=10000000, label="ADD AMOUNT")
