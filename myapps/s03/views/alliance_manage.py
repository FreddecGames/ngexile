# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---

        if not self.allianceId or not (self.hasRight('can_manage_description') or self.hasRight('can_manage_announce')):
            return HttpResponseRedirect('/s03/')
        
        #---

        return super().dispatch(request, *args, **kwargs)

    ################################################################################

    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'save' and (self.hasRight('can_manage_description') or self.hasRight('can_manage_announce')):
            
            logo = request.POST.get('logo', '').strip()
            if logo != '':
                if not isValidURL(logo):
                    messages.error(request, 'logo_invalid')
                    return HttpResponseRedirect('/s03/alliance-manage/')
            
            description = request.POST.get('description', '').strip()
        
            motd = request.POST.get('motd').strip()
            defcon = int(request.POST.get('defcon', 5))
    
            dbQuery('UPDATE alliances SET logo_url=' + dosql(logo) + ', description=' + dosql(description) + ', defcon=' + str(defcon) + ', announce=' + dosql(motd) + ' WHERE id = ' + str(self.allianceId))

        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, 'alliance-manage')
        
        self.selectedMenu = 'alliance'
        
        #---

        if self.allianceRights['leader'] or self.allianceRights['can_manage_description']: tpl.set('cat2')
        if self.allianceRights['leader'] or self.allianceRights['can_manage_announce']: tpl.set('cat1')
        
        #---
        
        query = ' SELECT description, logo_url, max_members, announce, defcon' + \
                ' FROM alliances' + \
                ' WHERE id=' + str(self.allianceId)
        alliance = dbRow(query)

        tpl.set('alliance', alliance)
        
        #---
        
        return self.display(tpl, request)
        