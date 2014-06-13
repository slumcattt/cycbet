from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, ModelForm, CharField,RadioSelect,CheckboxInput,Select,TextInput, HiddenInput, Textarea, SelectMultiple,DateTimeInput, DateTimeField, DateField, DateInput, ModelChoiceField,ModelMultipleChoiceField
from models import *

class Odds(ModelForm):
    error_css_class = 'error'
    exclude = ['',]
    class Meta:
        model = StageRider

class Bets(ModelForm):
    error_css_class = 'error'
    exclude = ['',]
    class Meta:
        model = Bet
        widgets = {
            'amt': TextInput(attrs={'class':'bet_amt',}),
            'status': HiddenInput(),
            'parlay':CheckboxInput(attrs={'class':'parlay'}),
            'user':HiddenInput(),
            'offer':HiddenInput(),
            'bet_cat':HiddenInput(),
            'id':HiddenInput(),
            }


