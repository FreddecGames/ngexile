# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsNotInMaintenance, IsOnHolidays ]

    ################################################################################

    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'unlock':
        
            dbQuery('SELECT sp_stop_holidays(' + str(self.userId) + ')')
            return HttpResponseRedirect('/s03/empire-view/')
        
        #---
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    ################################################################################
        
    def get(self, request, *args, **kwargs):

        #---

        tpl = getTemplate()

        #---

        query = 'SELECT username,' + \
                ' (SELECT int4(date_part(\'epoch\', min_end_time - now())) FROM users_holidays WHERE userid = id) AS min_time,' + \
                ' (SELECT int4(date_part(\'epoch\', end_time - now())) FROM users_holidays WHERE userid = id) AS remaining_time' + \
                ' FROM users WHERE privilege = -2 AND id=' + str(self.userId)
        row = dbRow(query)
        
        tpl.set('user', row)
        
        #---
        
        return Response(tpl.data)
