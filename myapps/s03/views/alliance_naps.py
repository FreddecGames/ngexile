# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not self.allianceId:
            return HttpResponseRedirect('/s03/alliance/')
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        if self.allianceRights['can_create_nap']:
        
            tag = request.POST.get('tag', '').strip()
            hours = int(request.POST.get('hours', 0))

            result = dbExecute('SELECT sp_alliance_nap_request(' + str(self.userId) + ',' + dosql(tag) + ',' + str(hours) + ')')
            
            if result == 1: messages.error(request, 'norights')
            elif result == 2: messages.error(request, 'unknown')
            elif result == 3: messages.error(request, 'already_naped')
            elif result == 4: messages.error(request, 'request_waiting')
            elif result == 6: messages.error(request, 'already_requested')
            
        return HttpResponseRedirect('/s03/alliance-naps/')
        
    def get(self, request, *args, **kwargs):
    
        action = request.GET.get('a', '')
        targetalliancetag = request.GET.get('tag', '').strip()
        
        if self.allianceRights['can_create_nap'] and action == 'accept':        
            dbQuery('SELECT sp_alliance_nap_accept(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')

        elif self.allianceRights['can_create_nap'] and action == 'decline':
            dbQuery('SELECT sp_alliance_nap_decline(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')
            
        elif self.allianceRights['can_create_nap'] and action == 'cancel':
            dbQuery('SELECT sp_alliance_nap_cancel(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')
            
        elif self.allianceRights['can_create_nap'] and action == 'sharelocs':
            dbQuery('SELECT sp_alliance_nap_toggle_share_locs(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')
            
        elif self.allianceRights['can_create_nap'] and action == 'shareradars':
            dbQuery('SELECT sp_alliance_nap_toggle_share_radars(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')
            
        elif self.allianceRights['can_break_nap'] and action == 'break':
        
            result = dbExecute('SELECT sp_alliance_nap_break(' + str(self.userId) + ',' + dosql(targetalliancetag) + ')')

            if result == 1: messages.error(request, 'norights')
            elif result == 2: messages.error(request, 'unknown')
            elif result == 3: messages.error(request, 'nap_not_found')
            elif result == 4: messages.error(request, 'not_enough_credits')
        
        #---
        
        content = getTemplate(self.request, 's03/alliance-naps')
        
        self.selectedMenu = 'alliance.naps'

        #---
        
        if self.allianceRights['can_create_nap']: content.Parse('can_create')
        if self.allianceRights['can_break_nap']: content.Parse('can_break')

        #---
        
        query = 'SELECT n.allianceid2, tag, name,' + \
                ' (SELECT COALESCE(sum(score)/1000, 0) AS score FROM users WHERE alliance_id=allianceid2), n.created, date_part(\'epoch\', n.break_interval)::integer AS break_interval, date_part(\'epoch\', break_on-now())::integer AS breaking_time,' + \
                ' share_locs, share_radars' + \
                ' FROM alliances_naps n' + \
                '  INNER JOIN alliances ON (allianceid2 = alliances.id)' + \
                ' WHERE allianceid1=' + str(self.allianceId) + \
                ' ORDER BY tag'
        naps = dbRows(query)
        content.setValue('naps', naps)

        #---

        query = 'SELECT alliances.tag, alliances.name, alliances_naps_offers.created, recruiters.username, declined, date_part(\'epoch\', break_interval)::integer AS break_interval' + \
                ' FROM alliances_naps_offers' + \
                '  INNER JOIN alliances ON alliances.id = alliances_naps_offers.allianceid' + \
                '  LEFT JOIN users AS recruiters ON recruiters.id = alliances_naps_offers.recruiterid' + \
                ' WHERE targetallianceid=' + str(self.allianceId) + ' AND NOT declined' + \
                ' ORDER BY created DESC'
        propositions = dbRows(query)
        content.setValue('propositions', propositions)

        #---
        
        query = 'SELECT alliances.tag, alliances.name, alliances_naps_offers.created, recruiters.username, declined, date_part(\'epoch\', break_interval)::integer' + \
                ' FROM alliances_naps_offers' + \
                '  INNER JOIN alliances ON alliances.id = alliances_naps_offers.targetallianceid' + \
                '  LEFT JOIN users AS recruiters ON recruiters.id = alliances_naps_offers.recruiterid' + \
                ' WHERE allianceid=' + str(self.allianceId) + \
                ' ORDER BY created DESC'
        requests = dbRows(query)
        content.setValue('requests', requests)

        return self.display(content)
