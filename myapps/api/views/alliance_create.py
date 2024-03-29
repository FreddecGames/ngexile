# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive, HasNoAlliance ]

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.data['action']
        
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

        tpl = getTemplate()
        
        #---

        tpl.set('can_join_alliance', self.profile['can_join_alliance'])
    
        #---

        return Response(tpl.data)
