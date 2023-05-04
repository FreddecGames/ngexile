# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GetView):
    
    template_name = 'ranking_player'
    
    def display(self, request):

        self.tpl.setValue('menu_selected', 'ranking')
