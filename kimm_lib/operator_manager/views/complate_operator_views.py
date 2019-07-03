from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView

# from operator_manager.forms. import *
from operator_manager.models.operator import Operator
from operator_manager.models.position import Position

from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
from accounts.views.admincheck import admincheck


import datetime

class CompleteOperatorView(TemplateView):
    model = Operator
    template_name ='operator_manager/complate_operator.html'

    def get(self, request, **kwargs):
        #アドミンチェック
        c = admincheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
