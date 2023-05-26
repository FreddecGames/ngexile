# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):

    ################################################################################

    def dispatch(self, request, fleetId):

        #---

        response = super().pre_dispatch(request)
        if response: return response
                
        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def post(self, request, fleetId):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'split':

            name = request.POST.get('name')
            if not isValidName(name):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            fleet = dbRows('SELECT * FROM vw_fleets WHERE id=' + str(fleetId))        
        
            newFleetId = dbExecute('SELECT fleet_create(' + str(self.userId) + ',' + str(fleet['planet_id']) + ',' + strSql(name) + ')')
            if newFleetId < 0:
                messages.error(request, 'fleet_create_error_' + str(newFleetId))
                return HttpResponseRedirect(request.build_absolute_uri())
            
            shipIds = dbRows('SELECT id FROM db_ships')
            for shipId in shipIds:
            
                count = int(request.POST.get('ship' + str(shipId['id']), 0))
                if count > 0:
                
                    result = dbExecute('SELECT * FROM fleet_ship_add(' + str(self.userId) + ',' + str(newFleetId) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                    
                        dbQuery('DELETE FROM fleets WHERE id=' + str(newFleetId) + ' AND profile_id=' + str(self.userId))
                        
                        messages.error(request, 'fleet_transfer_ship_to_fleet_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())
            
            newload = dbExecute('SELECT cargo_capacity FROM vw_fleets WHERE profile_id=' + str(self.userId) + ' AND id=' + str(newfleetid))
            
            ore = max(min(int(request.POST.get('load_ore', 0)), fleet['ore_count']), 0)
            hydro = max(min(int(request.POST.get('load_hydro', 0)), fleet['hydro_count']), 0)
            scientists = max(min(int(request.POST.get('load_scientists', 0)), fleet['scientist_count']), 0)
            soldiers = max(min(int(request.POST.get('load_soldiers', 0)), fleet['soldier_count']), 0)
            workers = max(min(int(request.POST.get('load_workers', 0)), fleet['worker_count']), 0)

            ore = min(ore, newload)
            newload = newload - ore

            hydro = min( hydro, newload)
            newload = newload - hydro

            scientists = min( scientists, newload)
            newload = newload - scientists

            soldiers = min( soldiers, newload)
            newload = newload - soldiers

            workers = min( workers, newload)
            newload = newload - workers

            if ore != 0 or hydro != 0 or scientists != 0 or soldiers != 0 or workers != 0:

                result = dbExecute('SELECT * FROM fleet_transfer_cargo_to_fleet(' + str(self.userId) + ',' + str(fleetId) + ',' + str(newFleetId) + ',' + str(ore) + ',' + str(hydro) + ',' + str(scientist) + ',' + str(soldier) + ',' + str(worker) + ')')
                if result > 0:
                    messages.error(request, 'fleet_transfer_cargo_to_fleet_error_' + str(result))
                    return HttpResponseRedirect(request.build_absolute_uri())
            
            shipIds = dbRows('SELECT id FROM db_ships')
            for shipId in shipIds:
            
                count = int(request.POST.get('ship' + str(shipId['id']), 0))
                if count > 0:
                
                    result = dbExecute('SELECT * FROM fleet_ship_remove(' + str(self.userId) + ',' + str(fleetId) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                    
                        dbQuery('DELETE FROM fleets WHERE id=' + str(newFleetId) + ' AND profile_id=' + str(self.userId))
                        
                        messages.error(request, 'fleet_ship_remove_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())
                        
            return HttpResponseRedirect('/ng0/fleet-view/?id=' + str(newfleetid))
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, fleetId):

        #---
        
        tpl = Template('fleet-split')

        self.selectedTab = 'split'
        self.selectedMenu = 'fleet'

        #---

        fleet = dbRows('SELECT * FROM vw_fleets WHERE id=' + str(fleetId))        
        tpl.set('fleet', fleet)

        #---

        ships = dbRows('SELECT * FROM vw_fleet_ships WHERE fleet_id=' + str(fleetId))        
        tpl.set('ships', ships)
        
        #---
         
        return self.display(request, tpl)
