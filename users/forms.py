from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from django.model import Habit

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email']

    # username = forms.CharField(min_length=5, max_length=50, required=True)
    # first_name = forms.CharField(max_length=50, required=True)
    # last_name = forms.CharField(max_length=50, required=True)
    # email = forms.EmailField(required=True)
    # password_1 = forms.PasswordInput()

