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

        tpl = Template('ranking-player')

        self.selectedTab = 'player'
        self.selectedMenu = 'ranking'

        #---
        
        players = dbRows('SELECT * FROM ng0.vw_ranking_players ORDER BY score')        
        tpl.set('players', players)
        
        #---

        return self.display(request, tpl)
