# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GetView):
    
    template_name = 'planet_view'
    
    def display(self, request):

        self.tpl.setValue('menu_selected', 'planet')
        self.tpl.setValue('tab_selected', 'view')
