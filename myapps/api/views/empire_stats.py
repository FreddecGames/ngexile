# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---

        tpl = getTemplate()

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

        return Response(tpl.data)
