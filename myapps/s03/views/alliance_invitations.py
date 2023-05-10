# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'accept' and self.profile['can_join_alliance'] and not self.allianceId:
        
            alliance_tag = request.POST.get('tag', '').strip()
            result = dbExecute('SELECT sp_alliance_accept_invitation(' + str(self.userId) + ',' + dosql(alliance_tag) + ')')
            if result == 0: return HttpResponseRedirect('/s03/alliance/')

            if result == 4: messages.error(request, 'max_members_reached')
            elif result == 6: messages.error(request, 'cant_rejoin_previous_alliance')
            
            return HttpResponseRedirect('/s03/alliance-invitations/')
            
        #---
            
        elif action == 'decline':
        
            alliance_tag = request.POST.get('tag', '').strip()
            dbQuery('SELECT sp_alliance_decline_invitation(' + str(self.userId) + ',' + dosql(alliance_tag) + ')')
            
        #---
        
        elif action == 'leave' and self.allianceId and self.profile['can_join_alliance']:
        
            dbQuery('SELECT sp_alliance_leave(' + str(self.userId) + ', 0)')
            return HttpResponseRedirect('/s03/alliance-view/')
        
        #---
        
        return HttpResponseRedirect('/s03/alliance-invitations/')

    def get(self, request, *args, **kwargs):
    
        #---

        content = getTemplate(request, 's03/alliance-invitations')
        
        if self.allianceId == None: self.selectedMenu = 'noalliance.invitations'
        else: self.selectedMenu = 'alliance.invitations'
        
        #---

        query = 'SELECT alliances.tag, alliances.name, alliances_invitations.created, users.username' + \
                ' FROM alliances_invitations' + \
                '  INNER JOIN alliances ON alliances.id = alliances_invitations.allianceid' + \
                '  LEFT JOIN users ON users.id = alliances_invitations.recruiterid' + \
                ' WHERE userid=' + str(self.userId) + ' AND NOT declined' + \
                ' ORDER BY created DESC'
        invitations = dbRows(query)
        content.setValue('invitations', invitations)
        
        #---

        if not self.profile['can_join_alliance']: content.Parse('cant_join')
        elif self.allianceId: content.Parse('cant_accept')
        
        #---

        if self.allianceId and self.profile['can_join_alliance']: content.Parse('can_leave')

        return self.display(content, request)
