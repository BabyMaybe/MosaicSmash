from django import forms
from django.forms import ModelForm
from django.forms import PasswordInput, DateInput, NumberInput, HiddenInput, TextInput
from django.contrib.auth.models import User



class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password','email']
        help_texts = {
            'username' : 'Name to use in tournament',
        }
        widgets = {
            'password' : PasswordInput(),
        }
