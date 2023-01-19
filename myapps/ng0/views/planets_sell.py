from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        action = request.POST.get('action', '').lower()
        if action == 'sell':
            
            planets = dbRows('SELECT id FROM nav_planet WHERE ownerid=' + str(self.profile['id']))
            for planet in planets:
                
                planetId = planet['id']
                
                ore = toInt(self.request.POST.get('o' + str(planetId)), 0)
                hydrocarbon = toInt(self.request.POST.get('h' + str(planetId)), 0)
                
                if ore > 0 or hydrocarbon > 0:
                
                    dbQuery('SELECT sp_market_sell(' + str(self.profile['id']) + ',' + str(planetId) + ',' + str(ore * 1000) + ',' + str(hydrocarbon * 1000) + ')')
        
        #--- get

        self.selectedMenu = 'planets'

        content = getTemplateContext(self.request, 'planets-sell')

        query = 'SELECT planets.id, planets.name, planets.galaxy, planets.sector, planets.planet, planets.floor,' + \
                ' planets.ore AS ore, planets.ore_production, planets.ore_capacity,' + \
                ' planets.hydrocarbon AS hydrocarbon, planets.hydrocarbon_production, planets.hydrocarbon_capacity,' + \
                ' (sp_market_price((sp_get_resource_price(0, galaxy)).sell_ore, planet_stock_ore))::real AS price_ore,' + \
                ' (sp_market_price((sp_get_resource_price(0, galaxy)).sell_hydrocarbon, planet_stock_hydrocarbon))::real AS price_hydrocarbon' + \
                ' FROM vw_planets AS planets' + \
                ' WHERE planets.floor > 0 AND planets.space > 0 AND planets.ownerid=' + str(self.profile['id']) + \
                ' ORDER BY planets.id'
        results = dbRows(query)
        planets = results
        
        for planet in planets:
            
            planet['img'] = getPlanetImg(planet['id'], planet['floor'])
            
            if planet['id'] == self.currentPlanet['id']: planet['is_current'] = True
            
            planet['ore_level'] = getPercent(planet['ore'], planet['ore_capacity'], 10)
            planet['hydrocarbon_level'] = getPercent(planet['hydrocarbon'], planet['hydrocarbon_capacity'], 10)

            planet['ore_max'] = min(10000, int(planet['ore'] / 1000))
            planet['hydrocarbon_max'] = min(10000, int(planet['hydrocarbon'] / 1000))
            
        content.assignValue('planets', planets)
            
        return self.display(content)
