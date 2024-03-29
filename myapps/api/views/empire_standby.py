# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---

        tpl = getTemplate()
        
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

        return Response(tpl.data)
