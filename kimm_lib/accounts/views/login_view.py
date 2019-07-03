from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from accounts.forms import *
from operator_manager.models.operator import Operator
from user_manager.models.user import User
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

class LoginView(TemplateView):
    def get(self, request):
        if 'id' not in request.session:
            form = LoginForm()
            params = {'form':form}
            return render(request, 'accounts/login.html', params)
        else:
            if request.session['mode'] == 'user_mode':
                return redirect(to='/book_rental/user_index')
            elif request.session['mode'] == 'operator_mode':
                return redirect(to='/book_manager/')



    def post(self, request):
        if self.request.POST['type'] == 'user':
            try:
                email = self.request.POST['email']
                pw = self.request.POST['pw']
                user = User.objects.get(email=email,password=pw,is_active=True)
                self.request.session['id'] = user.id
                self.request.session['mode'] = 'user_mode'
                return redirect(to='/book_rental/user_index')
            except:
                form = LoginForm(self.request.POST)
                word = '※e-mailまたはパスワードが間違っています'
                params = {'form':form, 'word':word}
                return render(request, 'accounts/login.html', params)

        if self.request.POST['type'] == 'operator':
            try:
                email = self.request.POST['email']
                pw = self.request.POST['pw']
                operator = Operator.objects.filter(email=email,password=pw,is_active=True).first()
                self.request.session['id'] = operator.id
                self.request.session['name'] = operator.full_name
                self.request.session['mode'] = 'operator_mode'
                return redirect(to='/book_manager/')
            except:
                form = LoginForm(self.request.POST, initial={'type':'operator'})
                word = '※e-mailまたはパスワードが間違っています'
                params = {'form':form, 'word':word}
                return render(request, 'accounts/login.html', params)
