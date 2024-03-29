# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'accept' and self.profile['can_join_alliance'] and not self.allianceId:
        
            alliance_tag = request.POST.get('tag', '').strip()
            result = dbExecute('SELECT sp_alliance_accept_invitation(' + str(self.userId) + ',' + dosql(alliance_tag) + ')')
            if result == 0: return HttpResponseRedirect('/s03/alliance-view/')

            if result == 4: messages.error(request, 'max_members_reached')
            elif result == 6: messages.error(request, 'cant_rejoin_previous_alliance')
            
        #---
            
        elif action == 'decline':
        
            alliance_tag = request.POST.get('tag', '').strip()
            dbQuery('SELECT sp_alliance_decline_invitation(' + str(self.userId) + ',' + dosql(alliance_tag) + ')')
            
        #---
        
        elif action == 'leave' and self.allianceId:
        
            dbQuery('SELECT sp_alliance_leave(' + str(self.userId) + ', 0)')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request, *args, **kwargs):
    
        #---

        tpl = getTemplate()
        
        #---

        query = 'SELECT alliances.tag, alliances.name, alliances_invitations.created, users.username' + \
                ' FROM alliances_invitations' + \
                '  INNER JOIN alliances ON alliances.id = alliances_invitations.allianceid' + \
                '  LEFT JOIN users ON users.id = alliances_invitations.recruiterid' + \
                ' WHERE userid=' + str(self.userId) + ' AND NOT declined' + \
                ' ORDER BY created DESC'
        invitations = dbRows(query)
        tpl.set('invitations', invitations)
        
        #---

        if not self.profile['can_join_alliance']: tpl.set('cant_join')
        elif self.allianceId: tpl.set('cant_accept')
        
        #---

        if self.allianceId: tpl.set('can_leave')

        #---
        
        return Response(tpl.data)
