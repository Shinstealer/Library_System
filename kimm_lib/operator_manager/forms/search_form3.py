from django import forms
from operator_manager.models import Operator
from django.contrib.auth.models import User
from django.core.validators import *


CHOICES3 = [
    ('id', 'ID'),
    ('name', '名前'),
    ('position', '役職'),
]

class SearchForm3(forms.Form):
    type = forms.ChoiceField(label='', required=True, choices=CHOICES3)
    find = forms.CharField(label='', required=True, widget=forms.TextInput())
