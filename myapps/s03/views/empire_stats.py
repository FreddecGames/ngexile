# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
    
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---

        tpl = getTemplate(request, 'empire-stats')

        self.selectedTab = 'stats'
        self.selectedMenu = 'empire'
        
        #---
        
        query = 'SELECT category, shipid, killed, lost, label' + \
                ' FROM users_ships_kills' + \
                '    INNER JOIN db_ships ON (db_ships.id = users_ships_kills.shipid)' + \
                ' WHERE userid=' + str(self.userId) + \
                ' ORDER BY shipid'
        results = dbRows(query)

        kills = 0
        losses = 0

        lastCategory = -1

        cats = []
        tpl.set('cats', cats)
        
        for result in results:
            
            if result['category'] != lastCategory:
                lastCategory = result['category']
                
                cat = { 'id':result['category'], 'ships':[] }
                cats.append(cat)
                
            cat['ships'].append(result)

            kills += result['killed']
            losses += result['lost']
        
        tpl.set('kills', kills)
        tpl.set('losses', losses)
        
        #---

        return self.display(tpl, request)
