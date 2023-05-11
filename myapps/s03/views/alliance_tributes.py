# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---

        if not self.allianceId:
            return HttpResponseRedirect('/s03/')
        
        #---

        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
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
        
        tpl = getTemplate(request, 'alliance-tributes')
        
        self.selectedMenu = 'alliance.tributes'

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
        
        return self.display(tpl, request)
