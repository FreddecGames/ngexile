# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):
        
        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        
        #---

        self.selectedMenu = "planets"

        content = getTemplate(self.request, "s03/planets")

        #---
        
        col = ToInt(request.GET.get("col"), 0)
        if col < 0 or col > 5: col = 0

        if col == 0: orderby = "id"
        elif col == 1: orderby = "upper(name)"
        elif col == 2: orderby = "ore_production"
        elif col == 3: orderby = "hydrocarbon_production"
        elif col == 4: orderby = "energy_consumption/(1.0+energy_production)"
        elif col == 5: orderby = "mood"
        
        content.setValue('col', col)

        #---
        
        reversed = False
        if request.GET.get("r", "") != "": reversed = not reversed
        
        content.setValue("reversed", reversed)

        #---

        if reversed: orderby = orderby + " DESC"
        orderby = orderby + ", upper(name)"
        
        query = "SELECT t.id, name, galaxy, sector, planet," + \
                "ore, ore_production, ore_capacity," + \
                "hydrocarbon, hydrocarbon_production, hydrocarbon_capacity," + \
                "(workers-workers_busy) AS workers_idle, workers_capacity," + \
                "(energy_production - energy_consumption) AS energy_production, energy_capacity," + \
                "floor, floor_occupied," + \
                "space, space_occupied," + \
                "commanderid, (SELECT name FROM commanders WHERE id = t.commanderid) AS commandername," + \
                "mod_production_ore, mod_production_hydrocarbon, workers, t.soldiers, soldiers_capacity," + \
                "t.scientists, scientists_capacity, workers_for_maintenance, planet_floor, mood," + \
                "energy, mod_production_energy, upkeep, energy_consumption," + \
                " (SELECT int4(COALESCE(sum(scientists), 0)) FROM planet_training_pending WHERE planetid=t.id) AS scientists_training," + \
                " (SELECT int4(COALESCE(sum(soldiers), 0)) FROM planet_training_pending WHERE planetid=t.id) AS soldiers_training," + \
                " credits_production, credits_random_production, production_prestige" + \
                " FROM vw_planets AS t" + \
                " WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.userId)+ \
                " ORDER BY " +orderby
        planets = dbRows(query)
        content.setValue("planets", planets)
        
        for planet in planets:
            
            planet["img"] = self.planetImg(planet['id'], planet['floor'])
            planet["credits"] = int((planet['credits_production'] + (planet['credits_random_production'] / 2)) * 24)
            planet["ore_level"] = self.getPercent(planet['ore'], planet['ore_capacity'], 10)
            planet["hydrocarbon_level"] = self.getPercent(planet['hydrocarbon'], planet['hydrocarbon_capacity'], 10)

            if planet['workers'] < planet['workers_for_maintenance']: planet["workers_low"] = True

            if planet['soldiers'] * 250 < planet['workers'] + planet['scientists']: planet["soldiers_low"] = True

            moodlevel = round(planet["mood"] / 10) * 10
            if moodlevel > 100: moodlevel = 100
            planet["mood_level"] = moodlevel
            
            mood_delta = 0
            if planet['commanderid']: mood_delta = mood_delta + 1
            if planet['soldiers'] * 250 >= planet['workers'] + planet['scientists']: mood_delta = mood_delta + 2
            else: mood_delta = mood_delta - 1
            planet["mood_delta"] = mood_delta
            
            planet["upkeep_soldiers"] = int((planet['workers'] + planet['scientists']) / 250)
        
        #---
        
        return self.display(content)
