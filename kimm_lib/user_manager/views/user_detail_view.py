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
from book_rental.models.wishbook import WishBook

class UserDetailView(DetailView):
    model = User
    template_name = 'user_manager/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        rental_list = Rental.objects.filter(user=user, return_date__isnull=True)
        context['rental_list'] = rental_list
        wish_history = WishBook.objects.filter(user=user, is_active=True)
        context['wish_history'] = wish_history
        return context

    def get(self, request, **kwargs):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
