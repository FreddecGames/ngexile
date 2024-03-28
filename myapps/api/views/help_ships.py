# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---

from rest_framework import permissions

class HomeWaitPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        
        dbConnect()
        
        #---
        
        query = 'SELECT privilege, resets' + \
                ' FROM users' + \
                ' WHERE id=' + str(request.user.id)
        row = dbRow(query)
        
        if not row or row['privilege'] != -3 or row['resets'] == 0:
            return False
        
        #---
        
        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']):        
            return False
        
        #---
        
        return True


class View(BaseView):
    permission_classes = [ IsAuthenticated, HomeWaitPermission ]


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
