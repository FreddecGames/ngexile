# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from myapps.s03.views._utils import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        
        #---
        
        self.userId = request.user.id
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        action = request.POST.get('action', '')
        if action == 'unlock':
            dbQuery('UPDATE users SET privilege=0 WHERE id=' + str(self.userId))
            return HttpResponseRedirect('/s03/overview/')
        
        return HttpResponseRedirect('/s03/wait/')
        
    def get(self, request, *args, **kwargs):

        tpl = getTemplate(self.request, 's03/wait')

        profile = dbRow('SELECT username, FROM users WHERE id=' + str(self.userId))
        tpl.setValue('profile', profile)

        return render(self.request, tpl.template, tpl.data)
