# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---

class View(BaseView):
    permission_classes = [ IsAuthenticated ]


    def get(self, request, format=None):
        
        data = {}
        
        #---
        
        query = ' SELECT privilege, resets, planets, credits_bankruptcy' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)        
        data = dbRow(query)
        
        #---
        
        if maintenance: data['maintenance'] = True
        
        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']): data['closed'] = True
        
        #---
        
        return Response(data)
