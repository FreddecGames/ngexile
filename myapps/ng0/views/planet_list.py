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
    
    def get(self, request):
        
        #---

        tpl = Template('planet-list')

        self.selectedTab = 'list'
        self.selectedMenu = 'planet'

        #---

        planets = dbRows('SELECT * FROM ng0.vw_planets WHERE profile_id=' + str(self.userId))        
        tpl.set('planets', planets)
        
        #---
        
        return self.display(request, tpl)
