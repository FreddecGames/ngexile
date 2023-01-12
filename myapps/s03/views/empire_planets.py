from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- get
        
        self.selectedMenu = 'planets'

        content = GetTemplate(self.request, 'empire-planets')
        
        query = 'SELECT planets.id, planets.name, planets.galaxy, planets.sector, planets.planet,' + \
                ' ore, ore_production, ore_capacity, mod_production_ore,' + \
                ' hydrocarbon, hydrocarbon_production, hydrocarbon_capacity, mod_production_hydrocarbon,' + \
                ' energy, (energy_production - energy_consumption) AS energy_balance, energy_capacity,' + \
                ' workers, workers_capacity, (workers - workers_busy) AS workers_idle, workers_for_maintenance,' + \
                ' scientists, scientists_capacity,' + \
                ' soldiers, soldiers_capacity,' + \
                ' floor_occupied, floor,' + \
                ' space_occupied, space,' + \
                ' commanderid, (SELECT name FROM commanders WHERE id = planets.commanderid) AS commandername,' + \
                ' upkeep, energy_consumption' + \
                ' FROM vw_planets AS planets' + \
                ' WHERE planets.floor > 0 AND planets.space > 0 AND planets.ownerid=' + str(self.UserId) + \
                ' ORDER BY planets.id'
        dbRows = oConnRows(query)
        
        list = []
        content.AssignValue('planets', list)
        
        for dbRow in dbRows:
        
            item = dbRow
            list.append(item)
            
            item['img'] = getPlanetImg(dbRow['id'], dbRow['floor'])
            
            if dbRow['id'] == self.CurrentPlanet: item['is_current'] = True
            
            item['ore_level'] = getPercent(dbRow['ore'], dbRow['ore_capacity'], 10)
            item['hydrocarbon_level'] = getPercent(dbRow['hydrocarbon'], dbRow['hydrocarbon_capacity'], 10)
            
            if dbRow['soldiers'] * 250 < dbRow['workers'] + dbRow['scientists']: item['soldiers_low'] = True
            item['soldiers_upkeep'] = int((dbRow['workers'] + dbRow['scientists']) / 250)

            if dbRow['mod_production_ore'] < 0 or dbRow['workers'] < dbRow['workers_for_maintenance']: item['ore_production_anormal'] = True
            if dbRow['mod_production_hydrocarbon'] < 0 or dbRow['workers'] < dbRow['workers_for_maintenance']: item['hydrocarbon_production_anormal'] = True
        
        return self.Display(content)
