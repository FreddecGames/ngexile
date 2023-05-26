# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):
    
    ################################################################################
    
    def dispatch(self, request):

        #---

        response = super().pre_dispatch(request)
        if response: return response

        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def post(self, request):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'create':
            
            techId = int(request.POST.get('tech', 0))
            
            result = dbExecute('SELECT * FROM profile_tech_pending_create(' + str(self.userId) + ',' + str(techId) + ')')
            if result > 0:
                messages.error(request, 'profile_tech_pending_create_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
            
        #---
        
        elif action == 'cancel':
            
            techId = int(request.POST.get('tech', 0))

            result = dbExecute('SELECT * FROM profile_tech_pending_cancel(' + str(self.userId) + ',' + str(techId) + ')')
            if result > 0:
                messages.error(request, 'profile_tech_pending_cancel_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request):
        
        #---

        tpl = Template('tech-list')
        
        self.selectedTab = 'list'
        self.selectedMenu = 'tech'

        #---
        
        techs = dbRows('SELECT * FROM ng0.vw_profile_techs WHERE profile_id=' + str(self.userId))        
        tpl.set('techs', techs)
            
        #---
        
        return self.display(request, tpl)
