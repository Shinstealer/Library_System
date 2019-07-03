from django import forms
from operator_manager.models.operator import Operator
from user_manager.models.user import User
from django.core.validators import *



class RentalForm(forms.Form):
    id = forms.IntegerField(label='', required=True, min_value=1)
