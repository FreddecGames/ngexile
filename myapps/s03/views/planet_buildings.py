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
        
        action = request.GET.get('a', '').lower()
        
        #---
        
        if action == 'build':
            buildingId = ToInt(request.GET.get('b'), '')
            dbQuery('SELECT sp_start_building(' + str(self.userId) + ',' + str(self.currentPlanetId) + ', ' + str(buildingId) + ', false)')
            return HttpResponseRedirect('/s03/planet-buildings/')
        
        #---
        
        elif action== 'cancel':
            buildingId = ToInt(request.GET.get('b'), '')
            dbQuery('SELECT sp_cancel_building(' + str(self.userId) + ',' + str(self.currentPlanetId) + ', ' + str(buildingId) + ')')
            return HttpResponseRedirect('/s03/planet-buildings/')
        
        #---
        
        elif action== 'destroy':
            buildingId = ToInt(request.GET.get('b'), '')
            dbQuery('SELECT sp_destroy_building(' + str(self.userId) + ',' + str(self.currentPlanetId) + ',' + str(buildingId) + ')')
            return HttpResponseRedirect('/s03/planet-buildings/')
        
        #---
        
        self.showHeader = True
        self.selectedMenu = 'planet'        
        self.headerUrl = '/s03/planet-buildings/'
        
        content = getTemplate(request, 's03/buildings')
                
        #---
        
        query = 'SELECT mod_production_ore, mod_production_hydrocarbon, mod_production_energy,' + \
                ' (floor - floor_occupied) AS free_floor, (space - space_occupied) AS free_space,' + \
                ' ore, hydrocarbon, workers, scientists, soldiers, (workers - workers_busy) AS free_workers,' + \
                ' ore_capacity, hydrocarbon_capacity, workers_capacity, scientists_capacity, soldiers_capacity' + \
                ' FROM vw_planets' + \
                ' WHERE id=' + str(self.currentPlanetId)
        planet = dbRow(query)
        
        #---

        query = 'SELECT buildingid, quantity FROM planet_buildings WHERE quantity > 0 AND planetid=' + str(self.currentPlanetId)
        results = dbRows(query)
        
        planetBuildings = {}
        for result in results:
            planetBuildings[str(result['buildingid'])] = result['quantity']
            
        #---
        
        query = 'SELECT buildingid, required_buildingid' + \
                ' FROM db_buildings_req_building' + \
                '  INNER JOIN db_buildings ON (db_buildings.id=db_buildings_req_building.buildingid)' + \
                ' WHERE db_buildings.destroyable'
        results = dbRows(query)
        
        buildReqs = {}
        for result in results:
            if str(result['buildingid']) in planetBuildings:
                buildReqs[str(result['required_buildingid'])] = result['buildingid']
        
        #---
        
        query = 'SELECT vw_buildings.id, vw_buildings.category, vw_buildings.cost_prestige, vw_buildings.cost_ore, vw_buildings.cost_hydrocarbon, vw_buildings.workers, vw_buildings.floor, vw_buildings.space,' + \
                ' vw_buildings.construction_maximum, vw_buildings.quantity, vw_buildings.build_status, vw_buildings.construction_time, vw_buildings.destroyable, vw_buildings.production_ore, vw_buildings.production_hydrocarbon, vw_buildings.energy_production, vw_buildings.buildings_requirements_met, vw_buildings.destruction_time,' + \
                ' vw_buildings.upkeep, vw_buildings.energy_consumption, vw_buildings.buildable,' + \
                ' db_buildings.label, db_buildings.description, db_buildings.maintenance_factor,' + \
                ' db_buildings.storage_ore, db_buildings.storage_hydrocarbon, db_buildings.storage_workers, db_buildings.storage_scientists, db_buildings.storage_soldiers' + \
                ' FROM vw_buildings' + \
                '  INNER JOIN db_buildings ON db_buildings.id=vw_buildings.id' + \
                ' WHERE planetid=' + str(self.currentPlanetId) + ' AND ((vw_buildings.buildable AND vw_buildings.research_requirements_met) or vw_buildings.quantity > 0)' + \
                ' ORDER BY vw_buildings.category, vw_buildings.id'
        buildings = dbRows(query)
        
        categories = []
        content.setValue('categories', categories)

        lastCategory = -1
        
        for building in buildings:
            if building['quantity'] > 0 or building['buildings_requirements_met']:
                
                if building['category'] != lastCategory:
                    lastCategory = building['category']
                    
                    category = { 'id':building['category'], 'buildings':[] }
                    categories.append(category)
            
                category['buildings'].append(building)
                
                building['ore_modifier'] = int(building['production_ore'] * (planet['mod_production_ore'] - 100) / 100)
                building['hydro_modifier'] = int(building['production_hydrocarbon'] * (planet['mod_production_hydrocarbon'] - 100) / 100)
                building['energy_modifier'] = int(building['energy_production'] * (planet['mod_production_energy'] - 100) / 100)
                
                building['production_ore'] = int(building['production_ore'])
                building['production_hydrocarbon'] = int(building['production_hydrocarbon'])
                building['energy_production'] = int(building['energy_production'])
                
                building['workers_for_maintenance'] = int(building['workers'] * building['maintenance_factor'] / 100)
                
                if building['build_status']:                
                    building['isbuilding'] = True
                    building['remainingtime'] = building['build_status']
                    
                elif not building['buildable']:
                    building['limitreached'] = True
                    
                elif building['quantity'] > 0 and building['quantity'] >= building['construction_maximum']:
                    if building['quantity'] == 1: building['built'] = True
                    else: building['limitreached'] = True
                    
                elif not building['buildings_requirements_met']:        
                    building['buildings_required'] = True
        
                else:
                    building['build'] = True
        
                    if building['floor'] > planet['free_floor']:
                        building['not_enough_floor'] = True
                        building['build'] = False
                        
                    if building['space'] > planet['free_space']:
                        building['not_enough_space'] = True
                        building['build'] = False
                        
                    if building['cost_prestige'] > 0 and building['cost_prestige'] > self.profile['prestige_points']:
                        building['not_enough_prestige'] = True
                        building['build'] = False
                        
                    if building['cost_ore'] > 0 and building['cost_ore'] > planet['ore']:
                        building['not_enough_ore'] = True
                        building['build'] = False
                        
                    if building['cost_hydrocarbon'] > 0 and building['cost_hydrocarbon'] > planet['hydrocarbon']:
                        building['not_enough_hydrocarbon'] = True
                        building['build'] = False
                        
                    if building['workers'] > 0 and building['workers'] > planet['free_workers']:
                        building['not_enough_workers'] = True
                        building['build'] = False
                        
                if building['quantity'] > 0 and building['destroyable']:
        
                    if building['destruction_time']:
                        building['isdestroying'] = True
                        building['nextdestroytime'] = building['destruction_time']
                        
                    elif building['workers'] / 2 > planet['free_workers']:
                        building['workers_required'] = True
                        
                    elif str(building['id']) in buildReqs:
                        building['required'] = True
                        
                    elif planet['workers'] > planet['workers_capacity'] - building['storage_workers'] \
                      or planet['scientists'] > planet['scientists_capacity'] - building['storage_scientists'] \
                      or planet['soldiers'] > planet['soldiers_capacity'] - building['storage_soldiers'] \
                      or planet['ore'] > planet['ore_capacity'] - building['storage_ore'] \
                      or planet['hydrocarbon'] > planet['hydrocarbon_capacity'] - building['storage_hydrocarbon']:
                        building['capacity'] = True
                        
                    else:
                        building['destroy'] = True
                
        #---
        
        return self.display(content, request)
