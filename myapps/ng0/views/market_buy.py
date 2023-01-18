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

        self.selectedMenu = 'market'

        content = getTemplateContext(self.request, 'market-buy')

        query = 'SELECT planets.id, planets.name, planets.galaxy, planets.sector, planets.planet, planets.floor,' + \
                ' planets.ore AS ore_count, planets.ore_production, planets.ore_capacity,' + \
                ' planets.hydrocarbon AS hydrocarbon_count, planets.hydrocarbon_production, planets.hydrocarbon_capacity,' + \
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
        dbRows = dbRows(query)
        
        list = []
        content.assignValue('planets', list)
        
        i = 0
        for dbRow in dbRows:
        
            item = dbRow
            list.append(item)
            
            item['index'] = i
            item['img'] = getPlanetImg(dbRow['id'], dbRow['floor'])
            
            if dbRow['id'] == self.currentPlanet['id']: item['is_current'] = True
            
            item['ore_level'] = getPercent(dbRow['ore_count'], dbRow['ore_capacity'], 10)
            item['hydrocarbon_level'] = getPercent(dbRow['hydrocarbon_count'], dbRow['hydrocarbon_capacity'], 10)

            item['ore_max'] = int((dbRow['ore_capacity'] - dbRow['ore_count']) / 1000)
            item['hydrocarbon_max'] = int((dbRow['hydrocarbon_capacity'] - dbRow['hydrocarbon_count']) / 1000)
            
            if dbRow['buying_ore'] or dbRow['buying_hydrocarbon']:
                
                item['buying'] = True
                
            else:
                
                item['price_ore'] = str(dbRow['price_ore']).replace(',', '.')
                item['price_hydrocarbon'] = str(dbRow['price_hydrocarbon']).replace(',', '.')
                
                if not dbRow['has_merchants']: item['cant_buy_merchant'] = True
                elif dbRow['workers'] < dbRow['workers_for_maintenance'] / 2: item['cant_buy_worker'] = True
                elif dbRow['blocus']: item['cant_buy_enemy'] = True
                else: item['can_buy'] = True
            
            i = i + 1
            
        return self.display(content)
