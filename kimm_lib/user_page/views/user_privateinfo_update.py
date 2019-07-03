from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from user_page.forms.private_update_form import PrivateUpdateForm
from user_manager.models.user import User
from operator_manager.models.operator import Operator
from book_rental.models.rental import Rental

from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


import datetime


class UserPrivateInfoUpdateView(UpdateView):
    template_name ='user_page/private_info_update.html'
    model = User
    form_class = PrivateUpdateForm
    success_url=reverse_lazy('user_index')

    def get(self, request, *args, **kwargs):
        if self.request.session['id'] == int(self.kwargs['pk']):
            return UpdateView.get(self, request, *args, **kwargs)
        else:
            return redirect('private_info_update' ,pk = self.request.session['id'])
    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        password_check= form.cleaned_data.get('password_check')
        if password == password_check:
            result = super().form_valid(form)
            messages.success(
                self.request, '情報変更成功です')
            return result
        else:
            result = super().form_invalid(form)
            messages.warning(
                self.request,'パスワードチェックしてください！'
                )
            return result
