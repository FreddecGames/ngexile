# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        if self.allianceId:
            return HttpResponseRedirect('/s03/')
        
        #---

        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'create' and self.profile['can_join_alliance']:
    
            name = request.POST.get('alliancename', '').strip()
            if not isValidAllianceName(name):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())

            tag = request.POST.get('alliancetag', '').strip()
            if not isValidAllianceTag(tag):
                messages.error(request, 'tag_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            result = dbExecute('SELECT sp_create_alliance(' + str(self.userId) + ',' + dosql(name) + ',' + dosql(tag) + ', \'\')')
            if result >= -1:
                return HttpResponseRedirect('/s03/alliance/')
                
            if result == -2: messages.error(request, 'name_already_used')
            elif result == -3: messages.error(request, 'tag_already_used')

        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request, *args, **kwargs):
    
        #---

        tpl = getTemplate(request, 'alliance-create')

        self.selectedTab = 'create'
        self.selectedMenu = 'alliance'
        
        #---

        tpl.set('can_join_alliance', self.profile['can_join_alliance'])
    
        #---

        return self.display(tpl, request)
