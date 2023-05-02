# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not self.allianceId or not (self.allianceRights['leader'] or self.allianceRights['can_see_members_info']):
            return HttpResponseRedirect('/s03/alliance/')
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        if self.allianceRights['leader'] and request.POST.get('submit', '') != '':
        
            query = 'SELECT id' + \
                    ' FROM users' + \
                    ' WHERE alliance_id=' + str(self.allianceId)
            members = dbRows(query)

            for member in members:
                
                rankId = int(request.POST.get('member' + str(member['id']), 100))
                
                query = 'UPDATE users SET' + \
                        ' alliance_rank=' + str(rankId) + \
                        ' WHERE id=' + str(member['id']) + ' AND alliance_id=' + str(self.allianceId) + ' AND (alliance_rank > 0 OR id=' + str(self.userId) + ')'
                dbQuery(query)

            if int(request.POST.get('member' + str(self.userId), 100)) > 0:
                return HttpResponseRedirect('/s03/alliance/')
                
        return HttpResponseRedirect('/s03/alliance-members/')
        
    def get(self, request, *args, **kwargs):

        action = request.GET.get('a', '').strip()

        if action == 'kick' and self.allianceRights['can_kick_player']:
        
            self.username = request.GET.get('name').strip()
            dbQuery('SELECT sp_alliance_kick_member(' + str(self.userId) + ',' + dosql(self.username) + ')')
        
        #---
        
        content = getTemplate(request, 's03/alliance-members')
        
        self.selectedMenu = 'alliance.members'
        
        #---
        
        query = 'SELECT rankid, label' + \
                ' FROM alliances_ranks' + \
                ' WHERE enabled AND allianceid=' + str(self.allianceId) + \
                ' ORDER BY rankid'
        ranks = dbRows(query)
        content.setValue('ranks', ranks)
        
        #---

        col = ToInt(request.GET.get('col'), 1)
        if col < 1 or col > 7: col = 1

        if col == 1:
            orderby = 'upper(username)'
            reversed = False
        elif col == 2:
            orderby = 'score'
            reversed = True
        elif col == 3:
            orderby = 'colonies'
            reversed = True
        elif col == 4:
            orderby = 'credits'
            reversed = True
        elif col == 5:
            orderby = 'lastactivity'
            reversed = True
        elif col == 6:
            orderby = 'alliance_joined'
            reversed = True
        elif col == 7:
            orderby = 'alliance_rank'
            reversed = False

        content.setValue('col', col)
        
        #---
        
        if request.GET.get('r', '') != '': reversed = not reversed
        else: content.Parse('r' + str(col))

        #---

        if self.allianceRights['can_kick_player']:
            content.Parse('can_kick')
            
        #---

        if reversed: orderby = orderby + ' DESC'
        orderby = orderby + ', upper(username)'
        
        query = 'SELECT username, CASE WHEN id=' + str(self.userId)+' OR score_visibility >=1 THEN score ELSE 0 END AS score, int4((SELECT count(1) FROM nav_planet WHERE ownerid=users.id)) AS colonies,' + \
                ' date_part(\'epoch\', now()-lastactivity) / 3600 AS lastactivity, alliance_joined, alliance_rank, privilege, score-previous_score AS score_delta, id,' + \
                ' 0, credits, score_visibility, orientation, COALESCE(date_part(\'epoch\', leave_alliance_datetime-now()), 0) AS leaving_time' + \
                ' FROM users' + \
                ' WHERE alliance_id=' + str(self.allianceId) + \
                ' ORDER BY ' + orderby
        members = dbRows(query)
        content.setValue('members', members)

        totalColonies = 0
        totalCredits = 0
        totalScore = 0
        totalScoreDelta = 0

        for member in members:
        
            totalColonies += member['colonies']
            totalCredits += member['credits']

            if member['score_visibility'] >= 1 or member['id'] == self.userId:
            
                totalScore = totalScore + member['score']
                totalScoreDelta = totalScoreDelta + member['score_delta']
                
                member['scoreShown'] = True

            if member['privilege'] == -1: member['banned'] = True
            elif member['privilege'] == -2: member['onholidays'] = True
            
            if member['lastactivity'] < 0.25: member['online'] = True
            elif member['lastactivity'] < 1: member['less1h'] = True
            elif member['lastactivity'] < 1 * 24: member['hours'] = True
            elif member['lastactivity'] < 7 * 24: member['days'] = int(member['lastactivity'] / 24)
            elif member['lastactivity'] <= 14*24: member['1weekplus'] = True
            elif member['lastactivity'] > 14*24: member['2weeksplus'] = True

            if self.allianceRights['leader'] and (member['alliance_rank'] > self.allianceRankId or member['id'] == self.userId):
                member['can_manage'] = True
                
            if self.allianceRights['can_kick_player'] and member['alliance_rank'] > self.allianceRankId:
                member['can_kick'] = True
            
        #---

        content.setValue('total_colonies', totalColonies)
        content.setValue('total_credits', totalCredits)
        content.setValue('total_score', totalScore)
        content.setValue('total_score_delta', totalScoreDelta)

        return self.display(content, request)
