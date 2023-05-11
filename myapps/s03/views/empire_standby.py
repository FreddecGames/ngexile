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

        tpl = getTemplate(request, 'empire-standby')
        
        self.selectedMenu = 'fleets.standby'
        
        #---
        
        query = 'SELECT nav_planet.id AS planet_id, nav_planet.name AS planet_name, nav_planet.galaxy, nav_planet.sector, nav_planet.planet, shipid, quantity, label' + \
                ' FROM planet_ships' + \
                '    INNER JOIN nav_planet ON (planet_ships.planetid = nav_planet.id)' + \
                '    INNER JOIN db_ships ON (db_ships.id = planet_ships.shipid)' + \
                ' WHERE nav_planet.ownerid =' + str(self.userId) + \
                ' ORDER BY nav_planet.id, shipid'
        results = dbRows(query)

        lastplanetid = -1

        planets = []
        tpl.set('planets', planets)
        
        for result in results:
            
            if result['planet_id'] != lastplanetid:
                lastplanetid = result['planet_id']
                
                planet = result
                planet['ships'] = []
                planets.append(planet)
                
            planet['ships'].append(result)
        
        #---

        return self.display(tpl, request)
