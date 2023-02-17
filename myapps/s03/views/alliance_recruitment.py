# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not self.allianceId or not (self.allianceRights["leader"] or self.allianceRights["can_see_members_info"]):
            return HttpResponseRedirect('/s03/alliance/')
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        if self.allianceRights["can_invite_player"]:
        
            name = request.POST.get("name", "").strip()
            result = dbExecute("SELECT sp_alliance_invite(" + str(self.userId) + "," + dosql(name) + ")")

            if result == 1: messages.error(request, 'no_right')
            elif result == 2: messages.error(request, 'name_unknown')
            elif result == 3: messages.error(request, 'already_member')
            elif result == 5: messages.error(request, 'already_invited')
            elif result == 6: messages.error(request, 'impossible')
        
        return HttpResponseRedirect('/s03/alliance-recruitment/')
        
    def get(self, request, *args, **kwargs):
        
        content = getTemplate(self.request, 's03/alliance-recruitment')

        self.selectedMenu = "alliance.recruitment"
        
        content.setValue('can_invite', self.allianceRights["can_invite_player"])
        
        query = "SELECT recruit.username, created, recruiters.username, declined" + \
                " FROM alliances_invitations" + \
                "  INNER JOIN users AS recruit ON recruit.id = alliances_invitations.userid" + \
                "  LEFT JOIN users AS recruiters ON recruiters.id = alliances_invitations.recruiterid" + \
                " WHERE allianceid=" + str(self.allianceId) + \
                " ORDER BY created DESC"
        invitations = dbRows(query)
        content.setValue('invitations', invitations)
        
        return self.display(content)
