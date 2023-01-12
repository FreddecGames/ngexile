from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        action = request.POST.get('action', '').lower()
        if action == 'sell':
            
            planets = oConnRows('SELECT id FROM nav_planet WHERE ownerid=' + str(self.UserId))
            for planet in planets:
                
                planetId = planet['id']
                
                ore = ToInt(self.request.POST.get('o' + str(planetId)), 0)
                hydrocarbon = ToInt(self.request.POST.get('h' + str(planetId)), 0)
                
                if ore > 0 or hydrocarbon > 0:
                
                    oConnDoQuery('SELECT sp_market_sell(' + str(self.UserId) + ',' + str(planetId) + ',' + str(ore * 1000) + ',' + str(hydrocarbon * 1000) + ')')
        
        #--- get

        self.selected_menu = 'market'

        content = GetTemplate(self.request, 'market-sell')

        query = 'SELECT planets.id, planets.name, planets.galaxy, planets.sector, planets.planet, planets.floor,' + \
                ' planets.ore AS ore_count, planets.ore_production, planets.ore_capacity,' + \
                ' planets.hydrocarbon AS hydrocarbon_count, planets.hydrocarbon_production, planets.hydrocarbon_capacity,' + \
                ' (sp_market_price((sp_get_resource_price(0, galaxy)).sell_ore, planet_stock_ore)) AS price_ore,' + \
                ' (sp_market_price((sp_get_resource_price(0, galaxy)).sell_hydrocarbon, planet_stock_hydrocarbon)) AS price_hydrocarbon' + \
                ' FROM vw_planets AS planets' + \
                ' WHERE planets.floor > 0 AND planets.space > 0 AND planets.ownerid=' + str(self.UserId) + \
                ' ORDER BY planets.id'
        dbRows = oConnRows(query)
        
        list = []
        content.AssignValue('planets', list)
        
        i = 0
        for dbRow in dbRows:
        
            item = dbRow
            list.append(item)
            
            item['index'] = i
            item['img'] = self.planetimg(dbRow['id'], dbRow['floor'])
            
            if dbRow['id'] == self.CurrentPlanet: item['is_current'] = True
            
            item['ore_level'] = self.getpercent(dbRow['ore_count'], dbRow['ore_capacity'], 10)
            item['hydrocarbon_level'] = self.getpercent(dbRow['hydrocarbon_count'], dbRow['hydrocarbon_capacity'], 10)

            item['ore_max'] = min(10000, int(dbRow['ore_count'] / 1000))
            item['hydrocarbon_max'] = min(10000, int(dbRow['hydrocarbon_count'] / 1000))
            
            item['price_ore'] = str(dbRow['price_ore']).replace(',', '.')
            item['price_hydrocarbon'] = str(dbRow['price_hydrocarbon']).replace(',', '.')
            
            i = i + 1
            
        return self.Display(content)
