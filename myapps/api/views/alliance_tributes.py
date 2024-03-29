# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive, HasAlliance ]

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'create' and self.hasRight('can_create_nap'):
        
            tag = request.POST.get('tag', '').strip()
            credits = ToInt(request.POST.get('credits'), 0)

            result = dbExecute('SELECT sp_alliance_tribute_new(' + str(self.userId) + ',' + dosql(tag) + ',' + str(credits) + ')')
            
            if result == 1: messages.error(request, 'new_norights')
            elif result == 2: messages.error(request, 'new_unknown')
            elif result == 3: messages.error(request, 'new_already_exists')

        #---
        
        elif action == 'cancel' and self.hasRight('can_break_nap'):
        
            tag = request.POST.get('tag').strip()
            result = dbExecute('SELECT sp_alliance_tribute_cancel(' + str(self.userId) + ',' + dosql(tag) + ')')

            if result == 1: messages.error(request, 'norights')
            elif result == 2: messages.error(request, 'unknown')
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate()

        #---
        
        if self.hasRight('can_create_nap'): tpl.set('can_create')
        if self.hasRight('can_break_nap'): tpl.set('can_break')
        
        #---
        
        query = 'SELECT w.created, alliances.id, alliances.tag, alliances.name, w.credits' + \
                ' FROM alliances_tributes w' + \
                '    INNER JOIN alliances ON (target_allianceid = alliances.id)' + \
                ' WHERE allianceid=' + str(self.allianceId) + \
                ' ORDER BY tag'
        tributes = dbRows(query)
        tpl.set('sent_tributes', tributes)
        
        #---
        
        query = 'SELECT w.created, alliances.id, alliances.tag, alliances.name, w.credits, w.next_transfer' + \
                ' FROM alliances_tributes w' + \
                '  INNER JOIN alliances ON (allianceid = alliances.id)' + \
                ' WHERE target_allianceid=' + str(self.allianceId) + \
                ' ORDER BY tag'
        tributes = dbRows(query)
        tpl.set('received_tributes', tributes)
        
        #---
        
        return Response(tpl.data)
