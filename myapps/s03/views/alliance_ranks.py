# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not self.allianceId or not self.allianceRights['leader']:
            return HttpResponseRedirect('/s03/alliance/')
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
    
        query = 'SELECT rankid, leader' + \
                ' FROM alliances_ranks' + \
                ' WHERE allianceid=' + str(self.allianceId) + \
                ' ORDER BY rankid'
        ranks = dbRows(query)    
        
        for rank in ranks:
        
            name = request.POST.get('n' + str(rank['rankid'])).strip()
            if len(name) > 2:
            
                query = 'UPDATE alliances_ranks SET' + \
                        ' label=' + dosql(name) + \
                        ', is_default=NOT leader AND ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_0'), False)) + \
                        ', can_invite_player=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_1'), False)) + \
                        ', can_kick_player=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_2'), False)) + \
                        ', can_create_nap=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_3'), False)) + \
                        ', can_break_nap=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_4'), False)) + \
                        ', can_ask_money=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_5'), False)) + \
                        ', can_see_reports=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_6'), False)) + \
                        ', can_accept_money_requests=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_7'), False)) + \
                        ', can_change_tax_rate=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_8'), False)) + \
                        ', can_mail_alliance=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_9'), False)) + \
                        ', can_manage_description=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_10'), False)) + \
                        ', can_manage_announce=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_11'), False)) + \
                        ', can_see_members_info=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_12'), False)) + \
                        ', members_displayed=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_13'), False)) + \
                        ', can_order_other_fleets=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_14'), False)) + \
                        ', can_use_alliance_radars=leader OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_15'), False)) + \
                        ', enabled=leader OR EXISTS(SELECT 1 FROM users WHERE alliance_id=' + str(self.allianceId) + ' AND alliance_rank=' + str(rank['rankid']) + ' LIMIT 1) OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_enabled'), False)) + ' OR ' + str(ToBool(request.POST.get('c' + str(rank['rankid']) + '_0'), False)) + \
                        ' WHERE allianceid=' + str(self.allianceId) + ' AND rankid=' + str(rank['rankid'])
                dbQuery(query)
                
        return HttpResponseRedirect('/s03/alliance-ranks/')
        
    def get(self, request, *args, **kwargs):
        
        content = getTemplate(request, 's03/alliance-ranks')
        
        self.selectedMenu = 'alliance.ranks'
        
        #---

        query = 'SELECT rankid, label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, ' + \
                ' can_accept_money_requests, can_change_tax_rate, can_mail_alliance, is_default, members_displayed, can_manage_description, can_manage_announce, ' + \
                ' enabled, can_see_members_info, can_order_other_fleets, can_use_alliance_radars' + \
                ' FROM alliances_ranks' + \
                ' WHERE allianceid=' + str(self.allianceId) + \
                ' ORDER BY rankid'
        ranks = dbRows(query)
        content.setValue('ranks', ranks)
        
        for rank in ranks:

            if rank['leader']: rank['disabled'] = True

            if rank['leader'] or rank['enabled']: rank['checked_enabled'] = True

            if not rank['leader'] and rank['is_default']: rank['checked_0'] = True

            if rank['leader'] or rank['can_invite_player']: rank['checked_1'] = True
            if rank['leader'] or rank['can_kick_player']: rank['checked_2'] = True

            if rank['leader'] or rank['can_create_nap']: rank['checked_3'] = True
            if rank['leader'] or rank['can_break_nap']: rank['checked_4'] = True

            if rank['leader'] or rank['can_ask_money']: rank['checked_5'] = True
            if rank['leader'] or rank['can_see_reports']: rank['checked_6'] = True

            if rank['leader'] or rank['can_accept_money_requests']: rank['checked_7'] = True
            if rank['leader'] or rank['can_change_tax_rate']: rank['checked_8'] = True

            if rank['leader'] or rank['can_mail_alliance']: rank['checked_9'] = True

            if rank['leader'] or rank['can_manage_description']: rank['checked_10'] = True
            if rank['leader'] or rank['can_manage_announce']: rank['checked_11'] = True

            if rank['leader'] or rank['can_see_members_info']: rank['checked_12'] = True

            if rank['leader'] or rank['members_displayed']: rank['checked_13'] = True

            if rank['leader'] or rank['can_order_other_fleets']: rank['checked_14'] = True
            if rank['leader'] or rank['can_use_alliance_radars']: rank['checked_15'] = True
        
        return self.display(content, request)
