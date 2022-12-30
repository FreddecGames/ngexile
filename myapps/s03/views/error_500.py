# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views import View

class View(View):

    def dispatch(self, request, *args, **kwargs):
        return render(request, '500.html', None)
