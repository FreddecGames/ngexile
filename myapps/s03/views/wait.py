# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .exile import *
from .template import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.UserId = ToInt(self.request.session.get('user'), '')
        if self.UserId == '': return HttpResponseRedirect('/s03/')

        query = "SELECT username FROM users WHERE privilege=-3 AND id=" + str(self.UserId)
        oRs = oConnExecute(query)
        if oRs == None: return HttpResponseRedirect("/s03/")
        
        action = request.POST.get("unlock", "")

        if action != "":
            oConnDoQuery("UPDATE users SET privilege=0 WHERE id="+str(self.UserId))
            return HttpResponseRedirect("/s03/")

        content = GetTemplate(self.request, "wait")
        
        content.AssignValue("username", oRs[0])

        return render(self.request, content.template, content.data)
