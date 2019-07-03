from django import forms
from operator_manager.models import Operator
from django.contrib.auth.models import User
from django.core.validators import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets


class Operator_Form(forms.ModelForm):
    password_check=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Operator
        fields = [ 'email', 'full_name','password','password_check' ,'birthday' ,'position' ,'is_admin' , ]
        widgets ={
            'password' : forms.PasswordInput,
            'birthday': forms.SelectDateWidget(years=[x for x in range(1970, 2030)]),
        }
        labels = {
            'email' : 'メールアドレス',
            'full_name' : '氏名',
            'password' : 'パスワード',
            'password_check' : 'パスワード確認',
            'birthday' : '生年月日',
            'position' : '役職',
            'is_admin' : '管理者権限',
        }
        
    def clean_FIELD(self):
        clean_data = super(Operator_Form,self).clean()
        password = clean_data.get('password')
        password_check = clean_data.get('password_check')

        if password != password_check:
            raise forms.ValidationError(
                'パスワードをもう一度確認してください！'
            )
        return password
    
    
      