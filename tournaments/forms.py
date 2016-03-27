from django import forms
from django.forms import ModelForm
from django.forms import PasswordInput, DateInput, NumberInput, HiddenInput, TextInput
from django.contrib.auth.models import User

from .models import MatchEntry

class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password','email']
        help_texts = {
            'username' : None,
            'password' : None,
        }
        widgets = {
            'password' : PasswordInput(),
        }

class DataEntryForm(ModelForm):
    class Meta:
        model = MatchEntry
        fields = '__all__'
        exclude = ['match']

    def __init__(self, *args, **kwargs):
        super(DataEntryForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False


    #def clean_kos(self):
        #custom validation of ko field
