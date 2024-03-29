# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsNotInMaintenance, IsWaiting ]

    ################################################################################

    def post(self, request, format=None):
        
        data = {}
        
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'unlock':
        
            dbQuery('UPDATE users SET privilege=0 WHERE id=' + str(self.userId))
            
            return Response(data)
        
        #---
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    ################################################################################
        
    def get(self, request, format=None):

        #---

        tpl = getTemplate()

        #---

        query = 'SELECT username' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        row = dbRow(query)

        tpl.set('profile', row)
        
        #---
        
        return Response(tpl.data)
