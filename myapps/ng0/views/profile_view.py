# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):

    ################################################################################
    
    def dispatch(self, request, profileUsername):

        #---

        response = super().pre_dispatch(request)
        if response: return response
        
        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def get(self, request, profileUsername):
        
        #---

        tpl = Template('profile-view')
        
        self.selectedTab = 'view'
        self.selectedMenu = 'profile'
            
        #---

        profile = dbRows('SELECT * FROM ng0.vw_profile WHERE username=' + str(profileUsername))        
        tpl.set('profile', profile)

        #---

        return self.display(request, tpl)
