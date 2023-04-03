# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):

        query = "SELECT id FROM nav_planet WHERE ownerid=" + str(self.userId)
        planets = dbRows(query)

        for planet in planets:
            
            planetId = planet['id']
            
            ore = ToInt(self.request.POST.get("o" + str(planetId)), 0)
            hydrocarbon = ToInt(self.request.POST.get("h" + str(planetId)), 0)

            if ore > 0 or hydrocarbon > 0:

                query = "SELECT * FROM sp_buy_resources(" + str(self.userId) + "," + str(planetId) + "," + str(ore * 1000) + "," + str(hydrocarbon * 1000) + ")"
                dbQuery(query)
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    def get(self, request, *args, **kwargs):
                
        content = getTemplate(self.request, "s03/market-buy")
        
        #---
        
        get_planet = self.request.GET.get("planet", "").strip()
        if get_planet != "": get_planet = " AND v.id=" + dosql(get_planet)

        #---

        query = "SELECT v.id, v.name, v.galaxy, v.sector, v.planet, v.ore, v.hydrocarbon, v.ore_capacity, v.hydrocarbon_capacity, v.planet_floor," + \
                " v.ore_production, v.hydrocarbon_production," + \
                " m.ore AS ore_bought, m.hydrocarbon AS hydrocarbon_bought, m.ore_price, m.hydrocarbon_price," + \
                " int4(date_part('epoch', m.delivery_time-now()))," + \
                " sp_get_planet_blocus_strength(v.id) >= v.space AS blocus," + \
                " workers, workers_for_maintenance," + \
                " (SELECT has_merchants FROM nav_galaxies WHERE id=v.galaxy) as has_merchants," + \
                " (sp_get_resource_price(" + str(self.userId) + ", v.galaxy)).buy_ore::real AS p_ore," + \
                " (sp_get_resource_price(" + str(self.userId) + ", v.galaxy)).buy_hydrocarbon AS p_hydrocarbon" + \
                " FROM vw_planets AS v" + \
                "    LEFT JOIN market_purchases AS m ON (m.planetid=v.id)" + \
                " WHERE floor > 0 AND v.ownerid=" + str(self.userId) + get_planet + \
                " ORDER BY v.id"
        planets = dbRows(query)
        content.setValue("m_planets", planets)
        
        total = 0
        count = 0

        for planet in planets:
            
            img = 1 + (planet['planet_floor'] + planet['id']) % 21
            if img < 10: img = "0" + str(img)
            planet["img"] = img

            if planet['ore'] > planet['ore_capacity'] - 4 * planet['ore_production']: planet["high_ore_capacity"] = True
            if planet['hydrocarbon'] > planet['hydrocarbon_capacity'] - 4 * planet['hydrocarbon_production']: planet["high_hydrocarbon_capacity"] = True

            planet["ore_max"] = int((planet['ore_capacity'] - planet['ore']) / 1000)
            planet["hydrocarbon_max"] = int((planet['hydrocarbon_capacity'] - planet['hydrocarbon']) / 1000)

            planet["price_ore"] = str(planet['p_ore']).replace(",", ".")
            planet["price_hydrocarbon"] = str(planet['p_hydrocarbon']).replace(",", ".")

            if planet['ore_bought'] or planet['hydrocarbon_bought']:
            
                subtotal = planet['ore_bought'] / 1000 * planet['ore_price'] + planet['hydrocarbon_bought'] / 1000 * planet['hydrocarbon_price']
                total = total + subtotal

                planet["buying_price"] = int(subtotal)

                planet["buying"] = True
                planet["can_buy"] = True
                
            else:

                planet["buying_price"] = 0

                if not planet['has_merchants']: planet["cant_buy_merchants"] = True
                elif planet['workers'] < planet['workers_for_maintenance'] / 2: planet["cant_buy_workers"] = True
                elif planet['blocus']: planet["cant_buy_enemy"] = True
                else:
                
                    planet["buy"] = True
                    planet["can_buy"] = True

                    count = count + 1

            if planet['id'] == self.currentPlanetId: planet["highlight"] = True
        
        #---
        
        if get_planet != "":
        
            self.showHeader = True
            self.selectedMenu = "planet"
            self.headerUrl = '/s03/market-buy/'
            
            content.setValue("showHeader", self.showHeader)
            
        else:
        
            self.selectedMenu = "merchants"
        
            content.setValue("total", int(total))
        
        #---
        
        if count > 0: content.Parse("buy")
        
        #---
        
        return self.display(content)
