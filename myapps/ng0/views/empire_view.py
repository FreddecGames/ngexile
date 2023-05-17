# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GetView):
    
    tab_selected = 'view'
    menu_selected = 'empire'
    
    template_name = 'empire_view'
    
    ################################################################################
    
    def display(self, request):
        
        #---

        pass
        