# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive, HasAlliance ]

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---

        if not self.allianceId or not self.hasRight('can_see_members_info'):
            return HttpResponseRedirect('/s03/')
        
        #---

        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
    
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'invite' and self.hasRight('can_invite_player'):
        
            name = request.POST.get('name', '').strip()
            result = dbExecute('SELECT sp_alliance_invite(' + str(self.userId) + ',' + dosql(name) + ')')

            if result == 1: messages.error(request, 'no_right')
            elif result == 2: messages.error(request, 'name_unknown')
            elif result == 3: messages.error(request, 'already_member')
            elif result == 5: messages.error(request, 'already_invited')
            elif result == 6: messages.error(request, 'impossible')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---
        
        tpl = getTemplate()
        
        #---
        
        tpl.set('can_invite', self.hasRight('can_invite_player'))
        
        #---
        
        query = 'SELECT recruit.username AS name, created, recruiters.username AS recruiter' + \
                ' FROM alliances_invitations' + \
                '  INNER JOIN users AS recruit ON recruit.id = alliances_invitations.userid' + \
                '  LEFT JOIN users AS recruiters ON recruiters.id = alliances_invitations.recruiterid' + \
                ' WHERE allianceid=' + str(self.allianceId) + \
                ' ORDER BY created DESC'
        invitations = dbRows(query)
        tpl.set('invitations', invitations)
        
        #---
        
        return Response(tpl.data)
