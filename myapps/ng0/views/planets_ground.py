from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- get

        self.selectedMenu = 'planets'

        content = getTemplateContext(self.request, 'planets-ground')

        query = 'SELECT nav_planet.id, nav_planet.name, nav_planet.galaxy, nav_planet.sector, nav_planet.planet, shipid, quantity, label, floor' + \
                ' FROM planet_ships' + \
                '    INNER JOIN nav_planet ON (planet_ships.planetid = nav_planet.id)' + \
                '    INNER JOIN db_ships ON (planet_ships.shipid = db_ships.id)' + \
                ' WHERE nav_planet.ownerid =' + str(self.profile['id']) + \
                ' ORDER BY nav_planet.id, shipid'
        results = dbRows(query)

        planets = []
        lastPlanetId = -1
        
        for result in results:
            
            if result['id'] != lastPlanetId:
            
                planet = result
                
                planet['img'] = getPlanetImg(planet['id'], planet['floor'])
                planet['ships'] = []
                
                planets.append(planet)
                
                lastPlanetId = result['id']

            ship = result
            planet['ships'].append(ship)
            
        content.assignValue('planets', planets)

        return self.display(content)
