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
        
        if action == 'declare' and self.hasRight('can_create_nap'):
        
            tag = request.POST.get('tag', '').strip()
            result = dbExecute('SELECT sp_alliance_war_declare(' + str(self.userId) + ',' + dosql(tag) + ')')
            
            if result == 1: messages.error(request, 'new_norights')
            elif result == 2: messages.error(request, 'new_unknown')
            elif result == 3: messages.error(request, 'new_already_at_war')
            elif result == 9: messages.error(request, 'new_not_enough_credits')
        
        #---
        
        elif action == 'pay' and self.hasRight('can_create_nap'):
        
            tag = request.POST.get('tag', '').strip()
            result = dbExecute('SELECT sp_alliance_war_pay_bill(' + str(self.userId) + ',' + dosql(tag) + ')')

            if result == 1: messages.error(request, 'norights')
            elif result == 2: messages.error(request, 'unknown')        
            elif result == 3: messages.error(request, 'war_not_found')

        #---
        
        elif action == 'stop' and self.hasRight('can_break_nap'):

            tag = request.POST.get('tag', '').strip()
            result = dbExecute('SELECT sp_alliance_war_stop(' + str(self.userId) + ',' + dosql(tag) + ')')

            if result == 1: messages.error(request, 'norights')
            elif result == 2: messages.error(request, 'unknown')        
            elif result == 3: messages.error(request, 'war_not_found')
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, 'alliance-wars')

        self.selectedTab = 'wars'
        self.selectedMenu = 'alliance'

        #---
        
        if self.hasRight('can_create_nap'): tpl.set('can_create')
        if self.hasRight('can_break_nap'): tpl.set('can_break')

        #---

        query = 'SELECT w.created, alliances.id, alliances.tag, alliances.name, cease_fire_requested, date_part(\'epoch\', cease_fire_expire-now())::integer, w.can_fight < now() AS can_fight, True AS attacker, next_bill < now() + INTERVAL \'1 week\', sp_alliance_war_cost(allianceid2) AS cost, next_bill' + \
                ' FROM alliances_wars w' + \
                '  INNER JOIN alliances ON (allianceid2 = alliances.id)' + \
                ' WHERE allianceid1=' + str(self.allianceId) + \
                ' UNION ' + \
                'SELECT w.created, alliances.id, alliances.tag, alliances.name, cease_fire_requested, date_part(\'epoch\', cease_fire_expire-now())::integer, w.can_fight < now() AS can_fight, False AS attacker, False, 0, next_bill' + \
                ' FROM alliances_wars w' + \
                '  INNER JOIN alliances ON (allianceid1 = alliances.id)' + \
                ' WHERE allianceid2=' + str(self.allianceId) + \
                ' ORDER BY tag'
        wars = dbRows(query)
        tpl.set('wars', wars)

        #---

        if request.GET.get('action', '') == 'new':

            tag = request.GET.get('tag').strip()

            war = dbRow('SELECT id, tag, name, sp_alliance_war_cost(id) + (const_coef_score_to_war()*sp_alliance_value(' + str(self.allianceId) + '))::integer AS cost FROM alliances WHERE lower(tag)=lower(' + dosql(tag) + ')')
            if war == None:
            
                tpl.set('tag', tag)
                messages.error(request, 'unknown')
                
            else:
            
                tpl.set('newwar', war)
                tpl.set('newwar_confirm')

        #---

        return self.display(tpl, request)
