# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def get(self, request, *args, **kwargs):
                
        #---
        
        nation = request.GET.get('name', '').strip()
        if nation == '': nation = self.profile['username']
        
        if not isValidName(nation):
            return HttpResponseRedirect('/s03/profile-view/')
            
        #---

        tpl = getTemplate(request, 'profile-view')
        
        self.selectedMenu = 'profile'
            
        #---

        query = 'SELECT u.username, u.avatar_url, u.description, sp_relation(u.id, ' + str(self.userId) + ') AS relation, ' + \
                ' u.alliance_id, a.tag, a.name, u.id, GREATEST(u.regdate, u.game_started) AS regdate, r.label,' + \
                ' COALESCE(u.alliance_joined, u.regdate), u.alliance_taxes_paid, u.alliance_credits_given, u.alliance_credits_taken,' + \
                ' u.id' + \
                ' FROM users AS u' + \
                ' LEFT JOIN alliances AS a ON (u.alliance_id = a.id) ' + \
                ' LEFT JOIN alliances_ranks AS r ON (u.alliance_id = r.allianceid AND u.alliance_rank = r.rankid) ' + \
                ' WHERE upper(u.username) = upper(' + dosql(nation) + ') LIMIT 1'
        row = dbRow(query)

        #---
        
        if row == None:
            if nation != '':
                
                tpl = getTemplate(request, 'profile-search')
                
                query = 'SELECT username' + \
                        ' FROM users' + \
                        ' WHERE upper(username) ILIKE upper(' + str( '\'%' + nation + '%\'') + ')' + \
                        ' ORDER BY upper(username)'
                nations = dbRows(query)
                tpl.set('nations', nations)
                
                #---
                
                return self.display(tpl, request)
            
            else: return HttpResponseRedirect('/s03/nation/')

        #---
        
        tpl.set('nation', row)

        #---

        if row['relation'] > rFriend:

            if row['alliance_id'] == rAlliance: show_details = self.allianceRights['leader'] or self.allianceRights['can_see_members_info']
            else: show_details = True

            if show_details:
                
                #---
                
                query = 'SELECT name, galaxy, sector, planet FROM vw_planets WHERE ownerid=' + str(row['id']) + ' ORDER BY id'
                planets = dbRows(query)
                tpl.set('planets', planets)
                
                #---
                
                query = 'SELECT id, name, attackonsight, engaged, remaining_time, ' + \
                    ' planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, sp_relation(planet_ownerid, ownerid) AS planet_relation,' + \
                    ' destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_ownerid, destplanet_owner_name, sp_relation(destplanet_ownerid, ownerid) AS destplanet_relation,' + \
                    ' action, signature, sp_get_user_rs(ownerid, planet_galaxy, planet_sector), sp_get_user_rs(ownerid, destplanet_galaxy, destplanet_sector)' + \
                    ' FROM vw_fleets WHERE ownerid=' + str(row['id'])
                if row['relation'] == rAlliance and not self.allianceRights['leader']: query = query + ' AND action != 0'
                query = query + ' ORDER BY planetid, upper(name)'
                fleets = dbRows(query)
                tpl.set('fleets', fleets)
        
        #---

        nationId = row['id']
        
        query = 'SELECT alliance_tag, alliance_name, joined, \'left\'' + \
                ' FROM users_alliance_history' + \
                ' WHERE userid = ' + str(nationId) + ' AND joined > (SELECT GREATEST(regdate, game_started) FROM users WHERE privilege < 100 AND id=' + str(nationId) + ')' + \
                ' ORDER BY joined DESC'
        alliances = dbRows(query)
        tpl.set('alliances', alliances)

        #---

        return self.display(tpl, request)
