from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        action = request.POST.get('action', '').lower()
        if action == 'buy':
            
            planets = dbRows('SELECT id FROM nav_planet WHERE ownerid=' + str(self.profile['id']))
            for planet in planets:
                
                planetId = planet['id']
                
                ore = toInt(self.request.POST.get('o' + str(planetId)), 0)
                hydrocarbon = toInt(self.request.POST.get('h' + str(planetId)), 0)
                
                if ore > 0 or hydrocarbon > 0:
                
                    dbQuery('SELECT sp_buy_resources(' + str(self.profile['id']) + ',' + str(planetId) + ',' + str(ore * 1000) + ',' + str(hydrocarbon * 1000) + ')')
        
        #--- get

        self.selectedMenu = 'planets'

        content = getTemplateContext(self.request, 'market-buy')

        query = 'SELECT planets.id, planets.name, planets.galaxy, planets.sector, planets.planet, planets.floor,' + \
                ' planets.ore AS ore, planets.ore_production, planets.ore_capacity,' + \
                ' planets.hydrocarbon AS hydrocarbon, planets.hydrocarbon_production, planets.hydrocarbon_capacity,' + \
                ' market.ore AS buying_ore, market.hydrocarbon AS buying_hydrocarbon, market.ore_price, market.hydrocarbon_price,' + \
                ' int4(date_part(\'epoch\', market.delivery_time - now())),' + \
                ' (sp_get_planet_blocus_strength(planets.id) >= planets.space) AS blocus,' + \
                ' workers, workers_for_maintenance,' + \
                ' (SELECT has_merchants FROM nav_galaxies WHERE id = planets.galaxy) as has_merchants,' + \
                ' (sp_get_resource_price(' + str(self.profile['id']) + ', planets.galaxy)).buy_ore::real AS price_ore,' + \
                ' (sp_get_resource_price(' + str(self.profile['id']) + ', planets.galaxy)).buy_hydrocarbon::real AS price_hydrocarbon' + \
                ' FROM vw_planets AS planets' + \
                '    LEFT JOIN market_purchases AS market ON (market.planetid = planets.id)' + \
                ' WHERE planets.floor > 0 AND planets.space > 0 AND planets.ownerid=' + str(self.profile['id']) + \
                ' ORDER BY planets.id'
        results = dbRows(query)
        planets = results
        
        for planet in planets:
            
            planet['img'] = getPlanetImg(planet['id'], planet['floor'])
            
            if planet['id'] == self.currentPlanet['id']: planet['is_current'] = True
            
            planet['ore_level'] = getPercent(planet['ore'], planet['ore_capacity'], 10)
            planet['hydrocarbon_level'] = getPercent(planet['hydrocarbon'], planet['hydrocarbon_capacity'], 10)

            planet['ore_max'] = int((planet['ore_capacity'] - planet['ore']) / 1000)
            planet['hydrocarbon_max'] = int((planet['hydrocarbon_capacity'] - planet['hydrocarbon']) / 1000)
            
            if planet['buying_ore'] or planet['buying_hydrocarbon']:
                
                planet['buying'] = True
                
            else:
                
                if not planet['has_merchants']: planet['cant_buy_merchant'] = True
                elif planet['workers'] < planet['workers_for_maintenance'] / 2: planet['cant_buy_worker'] = True
                elif planet['blocus']: planet['cant_buy_enemy'] = True
                else: planet['can_buy'] = True
        
        content.assignValue('planets', planets)
            
        return self.display(content)
