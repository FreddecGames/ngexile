# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GetView):
    
    template_name = 'map_galaxy'
    
    def display(self, request):

        self.tpl.setValue('tab_selected', 'galaxy')
