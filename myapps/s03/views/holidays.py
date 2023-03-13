# -*- coding: utf-8 -*-
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
        
        action = request.POST.get("unlock", "")
        
        if action != "":
            dbQuery("SELECT sp_stop_holidays(" + str(self.userId) + ")")
            return HttpResponseRedirect("/s03/overview/")
        
        return HttpResponseRedirect('/s03/holidays/')
        
    def get(self, request, *args, **kwargs):

        tpl = getTemplate(self.request, 's03/holidays')

        query = "SELECT username," + \
                " (SELECT int4(date_part('epoch', min_end_time-now())) FROM users_holidays WHERE userid=id) AS min_time," + \
                " (SELECT int4(date_part('epoch', end_time-now())) FROM users_holidays WHERE userid=id) AS remaining_time" + \
                " FROM users WHERE privilege=-2 AND id=" + str(self.userId)
        user = dbRow(query)
        
        if user == None: return HttpResponseRedirect("/")
        if user['remaining_time'] <= 0: return HttpResponseRedirect("/s03/overview/")
        
        tpl.setValue('user', user)
        
        return render(self.request, tpl.template, tpl.data)
