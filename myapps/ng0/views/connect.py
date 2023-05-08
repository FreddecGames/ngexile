# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(BaseView):

    def get(self, request, *args, **kwargs):
        
        #---
        
        ipaddress = request.META.get('REMOTE_ADDR', '')
        useragent = request.META.get('HTTP_USER_AGENT', '')
        forwardedfor = request.META.get('HTTP_X_FORWARDED_FOR', '')
        
        account = dbRow('SELECT lastplanetid, privilege, resets FROM sp_account_connect(' + str(self.userId) + ', 1036,' + strSql(ipaddress) + ',' + strSql(forwardedfor) + ',' + strSql(useragent) + ', 0)')
        
        if account['privilege'] == -3 and account['resets'] == 0: return HttpResponseRedirect('/ng0/home-start/')
        elif account['privilege'] == -3: return HttpResponseRedirect('/ng0/home-wait/')
        
        #---
        
        return HttpResponseRedirect('/ng0/empire-view/')
