# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views import View

from .exile import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            
            rs = oConnExecute('SELECT id, lastplanetid, privilege, resets FROM sp_account_connect(' + str(request.user.id) + ', 1036,' + dosql(self.ipaddress) + ',' + dosql(self.forwardedfor) + ',' + dosql(self.useragent) + ', 0)');

            request.session[sUser] = rs[0]
            request.session[sPlanet] = rs[1]
            request.session[sLogonUserID] = rs[0]
            
            if not request.session.get("isplaying"):
                request.session["isplaying"] = True
            
            result = oConnExecute('SELECT username FROM users WHERE id=' + str(rs[0]))
            try:
                if not result[0]: oConnDoQuery('UPDATE users SET username=' + dosql(request.user.username) + ' WHERE username IS NULL AND id=' + str(rs[0]))
            except:
                return HttpResponseRedirect("/s03/start/")
                
            if(rs[2] == -3):
                return HttpResponseRedirect("/s03/wait/")
            elif(rs[2] == -2):
                return HttpResponseRedirect("/s03/holidays/")
            elif(rs[2] < 100 and rs[3] == 0):
                return HttpResponseRedirect("/s03/start/")
                
            return HttpResponseRedirect("/s03/overview/")

