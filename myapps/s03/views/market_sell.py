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
    
    def post(self, request, *args, **kwargs):
    
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'sell':

            query = 'SELECT id FROM nav_planet WHERE ownerid=' + str(self.userId)
            planets = dbRows(query)

            for planet in planets:
                
                planetId = planet['id']
                
                ore = ToInt(request.POST.get('o' + str(planetId)), 0)
                hydrocarbon = ToInt(request.POST.get('h' + str(planetId)), 0)

                if ore > 0 or hydrocarbon > 0:
                
                    dbQuery('SELECT sp_market_sell(' + str(self.userId) + ',' + str(planetId) + ',' + str(ore * 1000) + ',' + str(hydrocarbon * 1000) + ')')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---
        
        tpl = getTemplate(request, 'market-sell')
        
        #---
        
        get_planet = request.GET.get('planet', '').strip()
        if get_planet != '': get_planet = ' AND v.id=' + dosql(get_planet)

        #---

        query = 'SELECT id, name, galaxy, sector, planet, ore, hydrocarbon, ore_capacity, hydrocarbon_capacity, planet_floor,' + \
                ' ore_production, hydrocarbon_production,' + \
                ' (sp_market_price((sp_get_resource_price(0, galaxy)).sell_ore, planet_stock_ore)) AS p_ore,' + \
                ' (sp_market_price((sp_get_resource_price(0, galaxy)).sell_hydrocarbon, planet_stock_hydrocarbon))AS p_hydrocarbon' + \
                ' FROM vw_planets AS v' + \
                ' WHERE floor > 0 AND v.ownerid=' + str(self.userId) + get_planet + \
                ' ORDER BY v.id'
        planets = dbRows(query)
        tpl.set('m_planets', planets)
        
        total = 0
        count = 0

        for planet in planets:
        
            img = 1 + (planet['planet_floor'] + planet['id']) % 21
            if img < 10: img = '0' + str(img)
            planet['img'] = img

            planet['ore_price2'] = str(planet['p_ore']).replace( ',', '.')
            planet['hydrocarbon_price2'] = str(planet['p_hydrocarbon']).replace(',', '.')

            if planet['ore'] > planet['ore_capacity'] - 4 * planet['ore_production']: planet['high_ore_capacity'] = True
            if planet['hydrocarbon'] > planet['hydrocarbon_capacity'] - 4 * planet['hydrocarbon_production']: planet['high_hydrocarbon_capacity'] = True

            planet['ore_max'] = min(10000, int(planet['ore'] / 1000))
            planet['hydrocarbon_max'] = min(10000, int(planet['hydrocarbon'] / 1000))

            planet['selling_price'] = 0

            count = count + 1

            if planet['id'] == self.currentPlanetId: planet['highlight'] = True
        
        #---
        
        if get_planet != '':
        
            self.selectedTab = 'sell'
            self.selectedMenu = 'planet'
            
            self.showHeader = True
            self.headerUrl = '/s03/market-sell/'
            
            tpl.set('showHeader', self.showHeader)
            
        else:
        
            self.selectedTab = 'sell'
            self.selectedMenu = 'merchants'
        
            tpl.set('total', int(total))
        
        #---
        
        if count > 0: tpl.set('sell')
        
        #---

        return self.display(tpl, request)
