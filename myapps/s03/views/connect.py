# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views import View

from myapps.s03.views._utils import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
    
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
            
        rs = oConnExecute('SELECT id, lastplanetid, privilege, resets FROM sp_account_connect(' + str(request.user.id) + ', 1036,' + dosql(self.ipaddress) + ',' + dosql(self.forwardedfor) + ',' + dosql(self.useragent) + ', 0)');

        request.session[sPlanet] = rs[1]
        request.session[sPrivilege] = rs[2]
        
        if (rs[2] == -3): return HttpResponseRedirect("/s03/wait/")
        elif (rs[2] == -2): return HttpResponseRedirect("/s03/holidays/")
        elif (rs[2] < 100 and rs[3] == 0): return HttpResponseRedirect("/s03/start/")
        else: return HttpResponseRedirect("/s03/overview/")
