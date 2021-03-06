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

def usercheck(request):
    if 'id' in request.session:
        if request.session['mode'] == 'user_mode':
            return None
        else:
            return redirect(to='/accounts/logout/')
    else:
        return redirect(to='/accounts/logout/')
