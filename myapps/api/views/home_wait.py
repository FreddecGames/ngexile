# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---

class View(BaseView):

    def dispatch(self, request, format=None):

        #---
        
        query = 'SELECT privilege, resets' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        row = dbRow(query)
        
        if not row or row['privilege'] != -3 or row['resets'] == 0: return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        #---
        
        return super().dispatch(request, format)

    def post(self, request, format=None):
        
        data = {}
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'unlock':
        
            dbQuery('UPDATE users SET privilege=0 WHERE id=' + str(self.userId))
            
            return Response(data)
        
        #---
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):

        #---

        data = {}

        #---

        query = 'SELECT username' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        row = dbRow(query)

        data['profile'] = row
        
        #---
        
        return Response(data)
