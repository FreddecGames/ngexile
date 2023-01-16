from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        if self.AllianceId == None: return HttpResponseRedirect('/s03/alliance-view/')
        if not (self.oAllianceRights['leader'] or self.oAllianceRights['can_manage_description'] or self.oAllianceRights['can_manage_announce']): return HttpResponseRedirect('/s03/alliance-view/')
        
        #--- post
        
        action = self.request.POST.get('action', '')
        
        if action == 'save':
        
            query = 'SELECT rankid FROM alliances_ranks  WHERE allianceid=' + str(self.AllianceId) + ' ORDER BY rankid'
            dbRows = oConnRows(query)
            for dbRow in dbRows:
                
                name = self.request.POST.get('n' + str(dbRow['rankid']), '').strip()
                if len(name) > 2:
                    
                    query = 'UPDATE alliances_ranks SET' + \
                            ' label=' + dosql(name) + \
                            ', is_default=NOT leader AND ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_0'), False)) + \
                            ', can_invite_player=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_1'), False)) + \
                            ', can_kick_player=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_2'), False)) + \
                            ', can_create_nap=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_3'), False)) + \
                            ', can_break_nap=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_4'), False)) + \
                            ', can_ask_money=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_5'), False)) + \
                            ', can_see_reports=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_6'), False)) + \
                            ', can_accept_money_requests=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_7'), False)) + \
                            ', can_change_tax_rate=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_8'), False)) + \
                            ', can_mail_alliance=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_9'), False)) + \
                            ', can_manage_description=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_10'), False)) + \
                            ', can_manage_announce=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_11'), False)) + \
                            ', can_see_members_info=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_12'), True)) + \
                            ', members_displayed=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_13'), False)) + \
                            ', can_order_other_fleets=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_14'), False)) + \
                            ', can_use_alliance_radars=leader OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_15'), True)) + \
                            ', enabled=leader OR EXISTS(SELECT 1 FROM users WHERE alliance_id=' + str(self.AllianceId) + ' AND alliance_rank=' + str(dbRow['rankid'])+ ' LIMIT 1) OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_enabled'), False)) + ' OR ' + str(ToBool(self.request.POST.get('c' + str(dbRow['rankid']) + '_0'), False)) + \
                            ' WHERE allianceid=' + str(self.AllianceId) + ' AND rankid=' + str(dbRow['rankid'])
                    oConnDoQuery(query)
            
            return HttpResponseRedirect('/s03/alliance-ranks/')
            
        #--- get
        
        self.selectedMenu = 'alliance'

        content = GetTemplate(self.request, 'alliance-ranks')
        
        # current ranks
        
        query = 'SELECT rankid, label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, ' + \
                ' can_accept_money_requests, can_change_tax_rate, can_mail_alliance, is_default, members_displayed, can_manage_description, can_manage_announce, ' + \
                ' enabled, can_see_members_info, can_order_other_fleets, can_use_alliance_radars' + \
                ' FROM alliances_ranks' + \
                ' WHERE allianceid=' + str(self.AllianceId) + \
                ' ORDER BY rankid'
        dbRows = oConnRows(query)
        
        list = []
        content.AssignValue('ranks', list)
        
        for dbRow in dbRows:
            
            item = {}
            list.append(item)
            
            item['rank_id'] = dbRow['rankid']
            item['rank_label'] = dbRow['label']

            if dbRow['leader']: item['disabled'] = True

            if dbRow['leader'] or dbRow['enabled']: item['checked_enabled'] = True

            if not dbRow['leader'] or dbRow['is_default']: item['checked_0'] = True

            if dbRow['leader'] or dbRow['can_invite_player']: item['checked_1'] = True
            if dbRow['leader'] or dbRow['can_kick_player']: item['checked_2'] = True

            if dbRow['leader'] or dbRow['can_see_reports']: item['checked_6'] = True
            if dbRow['leader'] or dbRow['can_mail_alliance']: item['checked_9'] = True

            if dbRow['leader'] or dbRow['can_manage_description']: item['checked_10'] = True
            if dbRow['leader'] or dbRow['can_manage_announce']: item['checked_11'] = True

            if dbRow['leader'] or dbRow['members_displayed']: item['checked_13'] = True

        return self.Display(content)
