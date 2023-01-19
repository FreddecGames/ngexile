from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- get
        
        self.selectedMenu = 'planets'

        content = getTemplateContext(self.request, 'planets-view')
        
        query = 'SELECT planets.id, planets.name, planets.galaxy, planets.sector, planets.planet,' + \
                ' ore, ore_production, ore_capacity, mod_production_ore,' + \
                ' hydrocarbon, hydrocarbon_production, hydrocarbon_capacity, mod_production_hydrocarbon,' + \
                ' energy, (energy_production - energy_consumption) AS energy_balance, energy_capacity,' + \
                ' workers, workers_capacity, (workers - workers_busy) AS workers_idle, workers_for_maintenance,' + \
                ' scientists, scientists_capacity, (SELECT int4(COALESCE(sum(scientists), 0)) FROM planet_training_pending WHERE planetid = planets.id) AS scientists_training,' + \
                ' soldiers, soldiers_capacity, (SELECT int4(COALESCE(sum(soldiers), 0)) FROM planet_training_pending WHERE planetid = planets.id) AS soldiers_training,' + \
                ' floor_occupied, floor,' + \
                ' space_occupied, space,' + \
                ' commanderid,' + \
                ' upkeep' + \
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
            
            if planet['soldiers'] * 250 < planet['workers'] + planet['scientists']: planet['soldiers_low'] = True
            planet['soldiers_upkeep'] = int((planet['workers'] + planet['scientists']) / 250)

            if planet['mod_production_ore'] < 0 or planet['workers'] < planet['workers_for_maintenance']: planet['ore_production_anormal'] = True
            if planet['mod_production_hydrocarbon'] < 0 or planet['workers'] < planet['workers_for_maintenance']: planet['hydrocarbon_production_anormal'] = True
        
        content.assignValue('planets', planets)
        
        return self.display(content)
