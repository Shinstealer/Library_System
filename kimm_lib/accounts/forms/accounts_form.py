from django import forms
from operator_manager.models.operator import Operator
from user_manager.models.user import User
from django.core.validators import *


TYPE_CHOICES = [
    ('user', '一般ユーザ'),
    ('operator', 'オペレータユーザ'),
]

class LoginForm(forms.Form):
    type = forms.ChoiceField(label='ユーザタイプ', required=True, choices=TYPE_CHOICES)
    email = forms.EmailField(label='e-mail', required=True, widget=forms.TextInput(attrs={'placeholder':'emailを入力'}))
    pw = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'placeholder':'パスワード入力'}))
