# -*- coding: utf-8 -*-

from myapps.s03.views._utils import *

class View(BaseView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        query = 'SELECT privilege' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        row = dbRow(query)
        
        if not row or row['privilege'] != -2: return HttpResponseRedirect('/s03/')
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################

    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'unlock':
        
            dbQuery('SELECT sp_stop_holidays(' + str(self.userId) + ')')
            return HttpResponseRedirect('/s03/empire-view/')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
        
    def get(self, request, *args, **kwargs):

        #---

        tpl = getTemplate(request, 'home-holidays')

        #---

        query = 'SELECT username,' + \
                ' (SELECT int4(date_part(\'epoch\', min_end_time - now())) FROM users_holidays WHERE userid = id) AS min_time,' + \
                ' (SELECT int4(date_part(\'epoch\', end_time - now())) FROM users_holidays WHERE userid = id) AS remaining_time' + \
                ' FROM users WHERE privilege = -2 AND id=' + str(self.userId)
        row = dbRow(query)
        
        tpl.set('user', row)
        
        #---
        
        return render(request, tpl.template, tpl.data)
