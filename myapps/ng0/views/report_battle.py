# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):

    ################################################################################
    
    def dispatch(self, request, battleId):

        #---

        response = super().pre_dispatch(request)
        if response: return response
        
        #---

        return super().dispatch(request)
        
    ################################################################################
    
    def get(self, request, battleId):
            
        #---
        
        tpl = Template('report-battle')
    
        self.selectedTab = 'battle'
        self.selectedMenu = 'report'
        
        #---
        
        battle = dbRow('SELECT * FROM ng0.vw_battle WHERE id=' + str(battleId))        
        tpl.set('battle', battle)
        
        #---
        
        fleets = dbRows('SELECT * FROM ng0.vw_battle_fleets WHERE battle_id=' + str(battleId))        
        tpl.set('fleets', fleets)
        
        for fleet in fleets:
        
            fleet['ships'] = dbRows('SELECT * FROM ng0.vw_battle_fleet_ships WHERE battle_fleet_id=' + str(fleet['id']))
            
            for ship in ships:
        
                ship['kills'] = dbRows('SELECT * FROM ng0.vw_battle_fleet_ship_kills WHERE battle_fleet_ship_id=' + str(ship['id']))
        
        #---
        
        return self.display(request, tpl)
