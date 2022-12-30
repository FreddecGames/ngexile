# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .config import *
from .sql import *
from .functions import *

class ExileMixin(LoginRequiredMixin, BaseMixin):

    def pre_dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if maintenance: return HttpResponseRedirect('/s03/maintenance/')
        
        connectDB()
