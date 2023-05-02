# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import View

from myapps.s03.views._utils import *

class View(View):

    def dispatch(self, request, *args, **kwargs):
        
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        
        #---

        content = getTemplate(request, "s03/maintenance")
        
        #---

        return render(request, content.template, content.data)
