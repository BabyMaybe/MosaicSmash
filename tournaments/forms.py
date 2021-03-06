from django import forms
from django.forms import ModelForm
from django.forms import PasswordInput, DateInput, NumberInput, HiddenInput, TextInput
from django.contrib.auth.models import User

from .models import MatchEntry, Match

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

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('stage', 'omega', 'teams', 'items', 'match_type', 'time_length')
        # exclude = ('date_played','winner')


class DataEntryForm(ModelForm):
    class Meta:
        model = MatchEntry
        exclude = ['match', 'date_created']

        widgets = {
            'kos': forms.NumberInput(attrs={'placeholder' : '0'}),
            'falls': forms.NumberInput(attrs={'placeholder' : '0'})
        }

    def __init__(self, *args, **kwargs):
        super(DataEntryForm, self).__init__(*args, **kwargs)
        self.empty_permitted = False


    #def clean_kos(self):
        #custom validation of ko field
