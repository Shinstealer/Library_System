from django import forms
from operator_manager.models import Operator
from django.contrib.auth.models import User
from django.core.validators import *


CHOICES4 = [
    ('id', 'ID'),
    ('name', '名前'),
    ('address', '住所'),
    ('tell', '電話番号'),
]

class SearchForm4(forms.Form):
    type = forms.ChoiceField(label='', required=True, choices=CHOICES4)
    find = forms.CharField(label='', required=True, widget=forms.TextInput())
