# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from myapps.s03.views._utils import *

from myapps.s03.views.lib_battle import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        battlekey = request.GET.get("key", "")
        if battlekey == "": return HttpResponseRedirect("/s03/reports/")
        
        creator = ToInt(request.GET.get("by"), 0)
        if creator == 0: return HttpResponseRedirect("/s03/reports/")

        fromview = request.GET.get("v", "")
        if fromview == "": return HttpResponseRedirect("/s03/reports/")
        
        id = request.GET.get("id", "")
        if id == "": return HttpResponseRedirect("/s03/reports/")

        #oKeyRs = oConnExecute(" SELECT 1 FROM battles WHERE id=" + str(id)+" AND " +dosql(battlekey)+"=MD5(key||" + str(creator)+") ")
        #if oKeyRs == None: return HttpResponseRedirect("/s03/reports/")
        
        content = FormatBattle(self, id, creator, fromview, True)
        
        content.setValue("skin", "s_default")
        content.setValue("timers_enabled", "false")
        
        return render(self.request, content.template, content.data)
