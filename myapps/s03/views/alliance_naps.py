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
                
        if action == 'request' and self.hasRight('can_create_nap'):
        
            tag = request.POST.get('tag', '').strip()
            hours = ToInt(request.POST.get('hours'), 0)

            result = dbExecute('SELECT sp_alliance_nap_request(' + str(self.userId) + ',' + dosql(tag) + ',' + str(hours) + ')')
            
            if result == 1: messages.error(request, 'norights')
            elif result == 2: messages.error(request, 'unknown')
            elif result == 3: messages.error(request, 'already_naped')
            elif result == 4: messages.error(request, 'request_waiting')
            elif result == 6: messages.error(request, 'already_requested')
        
        #---
        
        elif action == 'accept' and self.hasRight('can_create_nap'):
        
            targetalliancetag = request.POST.get('tag', '').strip()
            dbQuery('SELECT sp_alliance_nap_accept(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')

        #---

        elif action == 'decline' and self.hasRight('can_create_nap'):

            targetalliancetag = request.POST.get('tag', '').strip()
            dbQuery('SELECT sp_alliance_nap_decline(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')
            
        #---

        elif action == 'cancel' and self.hasRight('can_create_nap'):

            targetalliancetag = request.POST.get('tag', '').strip()
            dbQuery('SELECT sp_alliance_nap_cancel(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')
            
        #---

        elif action == 'sharelocs' and self.hasRight('can_create_nap'):

            targetalliancetag = request.POST.get('tag', '').strip()
            dbQuery('SELECT sp_alliance_nap_toggle_share_locs(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')
            
        #---

        elif action == 'shareradars' and self.hasRight('can_create_nap'):

            targetalliancetag = request.POST.get('tag', '').strip()
            dbQuery('SELECT sp_alliance_nap_toggle_share_radars(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')
            
        #---

        elif action == 'break' and self.hasRight('can_break_nap'):
        
            targetalliancetag = request.POST.get('tag', '').strip()
            result = dbExecute('SELECT sp_alliance_nap_break(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')

            if result == 1: messages.error(request, 'norights')
            elif result == 2: messages.error(request, 'unknown')
            elif result == 3: messages.error(request, 'nap_not_found')
            elif result == 4: messages.error(request, 'not_enough_credits')
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, 'alliance-naps')
        
        self.selectedTab = 'naps'
        self.selectedMenu = 'alliance'

        #---
        
        if self.hasRight('can_create_nap'): tpl.set('can_create')
        if self.hasRight('can_break_nap'): tpl.set('can_break')

        #---
        
        query = 'SELECT n.allianceid2, tag, name,' + \
                ' (SELECT COALESCE(sum(score)/1000, 0) AS score FROM users WHERE alliance_id=allianceid2), n.created, date_part(\'epoch\', n.break_interval)::integer AS break_interval, date_part(\'epoch\', break_on-now())::integer AS breaking_time,' + \
                ' share_locs, share_radars' + \
                ' FROM alliances_naps n' + \
                '  INNER JOIN alliances ON (allianceid2 = alliances.id)' + \
                ' WHERE allianceid1=' + str(self.allianceId) + \
                ' ORDER BY tag'
        naps = dbRows(query)
        tpl.set('naps', naps)

        #---

        query = 'SELECT alliances.tag, alliances.name, alliances_naps_offers.created, recruiters.username, declined, date_part(\'epoch\', break_interval)::integer AS break_interval' + \
                ' FROM alliances_naps_offers' + \
                '  INNER JOIN alliances ON alliances.id = alliances_naps_offers.allianceid' + \
                '  LEFT JOIN users AS recruiters ON recruiters.id = alliances_naps_offers.recruiterid' + \
                ' WHERE targetallianceid=' + str(self.allianceId) + ' AND NOT declined' + \
                ' ORDER BY created DESC'
        propositions = dbRows(query)
        tpl.set('propositions', propositions)

        #---
        
        query = 'SELECT alliances.tag, alliances.name, alliances_naps_offers.created, recruiters.username, declined, date_part(\'epoch\', break_interval)::integer AS break_interval' + \
                ' FROM alliances_naps_offers' + \
                '  INNER JOIN alliances ON alliances.id = alliances_naps_offers.targetallianceid' + \
                '  LEFT JOIN users AS recruiters ON recruiters.id = alliances_naps_offers.recruiterid' + \
                ' WHERE allianceid=' + str(self.allianceId) + \
                ' ORDER BY created DESC'
        requests = dbRows(query)
        tpl.set('requests', requests)

        #---
        
        return self.display(tpl, request)
