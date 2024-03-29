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

        query = 'SELECT nav_planet.id AS planet_id, nav_planet.name AS planet_name, nav_planet.galaxy, nav_planet.sector, nav_planet.planet,' + \
                ' fleets.id, fleets.name, users.username, alliances.tag, sp_relation(fleets.ownerid, nav_planet.ownerid) AS relation, fleets.signature' + \
                ' FROM nav_planet' + \
                '    INNER JOIN fleets ON fleets.planetid=nav_planet.id' + \
                '    INNER JOIN users ON fleets.ownerid=users.id' + \
                '    LEFT JOIN alliances ON users.alliance_id=alliances.id' + \
                ' WHERE nav_planet.ownerid=' + str(self.userId) + ' AND fleets.ownerid != nav_planet.ownerid AND action != 1 AND action != -1' + \
                ' ORDER BY nav_planet.id, upper(alliances.tag), upper(fleets.name)'
        results = dbRows(query)

        lastplanetid = -1

        planets = []
        tpl.set('planets', planets)
        
        for result in results:
            
            if result['planet_id'] != lastplanetid:
                lastplanetid = result['planet_id']
                
                planet = result
                planet['fleets'] = []
                planets.append(planet)
                
            planet['fleets'].append(result)
        
        #---

        return Response(tpl.data)
