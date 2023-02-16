# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views import View

from myapps.s03.views._utils import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
    
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        
        self.userId = request.user.id
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        ipaddress = request.META.get('REMOTE_ADDR', '')
        useragent = request.META.get('HTTP_USER_AGENT', '')
        forwardedfor = request.META.get('HTTP_X_FORWARDED_FOR', '')
            
        account = dbRow('SELECT lastplanetid, privilege, resets FROM sp_account_connect(' + str(self.userId) + ', 1036,' + dosql(ipaddress) + ',' + dosql(forwardedfor) + ',' + dosql(useragent) + ', 0)');

        request.session[sPrivilege] = account['privilege']
        
        if (account['privilege'] == -3 and account['resets'] == 0): return HttpResponseRedirect('/s03/start/')
        elif (account['privilege'] == -3): return HttpResponseRedirect('/s03/wait/')
        elif (account['privilege'] == -2): return HttpResponseRedirect('/s03/holidays/')
        
        else: return HttpResponseRedirect('/s03/overview/')
