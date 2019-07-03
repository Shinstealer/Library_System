from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView

from user_manager.models.user import User
from book_rental.models.rental import Rental

from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check


import datetime

class CheckUserView(DetailView):
    template_name ='user_manager/check_user.html'
    model = User
    def post(self, request, *args, **kwargs):
        #レンタルがないかを確認する
        records = Rental.objects.all()
        for record in records:
            if record.user.id == int(self.kwargs['pk']):
                return redirect(to = '/user_manager/error_user')

        #会員削を行う
        user = User.objects.get(id = self.kwargs['pk'])
        user.is_active = False
        user.leave_date = datetime.date.today()
        user.save()
        return redirect(to ='/user_manager/complete_user')

    def get(self, request, **kwargs):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
