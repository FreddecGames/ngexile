# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---

class View(BaseView):

    def get(self, request, format=None):
        
        data = {}
        
        #---

        query = 'SELECT username, credits, prestige_points, lastplanetid, deletion_date, planets, score, previous_score, mod_planets, mod_commanders,' + \
                ' alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance,' + \
                ' credits_bankruptcy, orientation' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)        
        result = dbRow(query)

        data['username'] = result['username']
        data['profile_credits'] = result['credits']
        data['profile_prestige_points'] = result['prestige_points']
        data['profile_alliance_id'] = result['alliance_id']
        data['profile_alliance_rank'] = result['alliance_rank']
        data['delete_datetime'] = result['deletion_date']
        data['bankruptcy_hours'] = result['credits_bankruptcy']
        data['cur_planetid'] = result['lastplanetid']
        
        #---
        
        if data['profile_alliance_id']:
        
            query = 'SELECT label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, can_accept_money_requests, can_change_tax_rate, can_mail_alliance,' + \
                    ' can_manage_description, can_manage_announce, can_see_members_info, can_use_alliance_radars, can_order_other_fleets' + \
                    ' FROM alliances_ranks' + \
                    ' WHERE allianceid=' + str(data['profile_alliance_id']) + ' AND rankid=' + str(data['profile_alliance_rank'])
            result = dbRow(query)
            
            data['profile_alliance_rights'] = result
        
        #---
        
        query = 'SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=' + str(self.userId) + ' AND read_date is NULL) AS new_mail,' + \
                '(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=' + str(self.userId) + ' AND read_date is NULL AND datetime <= now()) AS new_report'
        result = dbRow(query)
        
        data['new_mail'] = result['new_mail']
        data['new_report'] = result['new_report']
        
        #---

        query = 'SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=' + str(data['cur_planetid']) + ' AND ownerid=' + str(self.userId)
        result = dbRow(query)
        
        data['cur_g'] = result['galaxy']
        data['cur_s'] = result['sector']
        data['cur_p'] = ((data['cur_planetid']  - 1) % 25) + 1
        
        #---
        
        if request.user.is_impersonate:
        
            data['impersonating'] = True
        
        #---
        
        return Response(data)
