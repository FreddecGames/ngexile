# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not self.allianceId or not (self.allianceRights['leader'] or self.allianceRights['can_manage_description'] or self.allianceRights['can_manage_announce']):
            return HttpResponseRedirect('/s03/alliance/')
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        if request.POST.get('submit', '') != '':
        
            #---
        
            if self.allianceRights['can_manage_description']:
                
                logo = self.request.POST.get('logo', '').strip()
                if not isValidURL(logo):
                    messages.error(request, 'logo_invalid')
                    return HttpResponseRedirect('/s03/alliance-manage/')
                
                description = self.request.POST.get('description', '').strip()
                
                dbQuery('UPDATE alliances SET logo_url=' + dosql(logo) + ', description=' + dosql(description) + ' WHERE id = ' + str(self.allianceId))
        
            #---
        
            if self.allianceRights['can_manage_announce']:
            
                motd = self.request.POST.get('motd').strip()
                defcon = int(self.request.POST.get('defcon', 5))
                
                dbQuery('UPDATE alliances SET defcon=' + str(defcon) + ', announce=' + dosql(motd) + ' WHERE id = ' + str(self.allianceId))

        return HttpResponseRedirect('/s03/alliance-manage/')
                

    def get(self, request, *args, **kwargs):
        
        content = getTemplate(self.request, 's03/alliance-manage')
        
        self.selectedMenu = 'alliance.manage'
        
        #---

        if self.allianceRights['leader'] or self.allianceRights['can_manage_description']: content.Parse('cat2')
        if self.allianceRights['leader'] or self.allianceRights['can_manage_announce']: content.Parse('cat1')
        
        #---
        
        query = 'SELECT description, logo_url,' + \
                ' max_members' + \
                ' FROM alliances' + \
                ' WHERE id=' + str(self.allianceId)
        alliance = dbRow(query)

        query = 'SELECT announce, defcon FROM alliances WHERE id=' + str(self.allianceId)
        alliance |= dbRow(query)

        content.setValue('alliance', alliance)
        
        return self.display(content)
        