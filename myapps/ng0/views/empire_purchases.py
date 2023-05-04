# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GetView):
    
    template_name = 'empire_purchases'
    
    def display(self, request):

        self.tpl.setValue('menu_selected', 'empire')
        self.tpl.setValue('tab_selected', 'purchases')
