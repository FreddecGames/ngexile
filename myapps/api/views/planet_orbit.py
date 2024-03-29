# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]
    
    ################################################################################
    
    def post(self, request, *args, **kwargs):
    
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'create':

            fleetname = request.POST.get('name', '').strip()

            if not isValidObjectName(fleetname):
                messages.error(request, 'fleet_name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            fleetid = dbExecute('SELECT sp_create_fleet(' + str(self.userId) + ',' + str(self.currentPlanetId) + ',' + dosql(fleetname) + ')')

            if fleetid < 0:
            
                if fleetid == -3: messages.error(request, 'fleet_too_many')
                else: messages.error(request, 'fleet_name_already_used') 
                
                return HttpResponseRedirect(request.build_absolute_uri())
            
            cant_use_ship = False

            rows = dbRows('SELECT id FROM db_ships')
            for row in rows:
            
                quantity = ToInt(request.POST.get('s' + str(row['id'])), 0)
                if quantity > 0:
                
                    result = dbExecute('SELECT * FROM sp_transfer_ships_to_fleet(' + str(self.userId) + ', ' + str(fleetid) + ', ' + str(row['id']) + ', ' + str(quantity) + ')')
                    cant_use_ship = cant_use_ship or result == 3

            dbQuery('DELETE FROM fleets WHERE size=0 AND id=' + str(fleetid) + ' AND ownerid=' + str(self.userId))

            if cant_use_ship: messages.error(request, 'ship_cant_be_used')   
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
            
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate()

        self.showHeader = True
        
        #---
        
        query = 'SELECT id, name, engaged, size, signature,' + \
                ' planet_owner_name, planet_owner_relation,' + \
                ' action, (cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers) AS cargo' + \
                ' FROM vw_fleets ' + \
                ' WHERE planetid=' + str(self.currentPlanetId) +' AND action != 1 AND action != -1' + \
                ' ORDER BY upper(name)'
        fleets = dbRows(query)
        tpl.set('fleets', fleets)
        
        #---
        
        query = 'SELECT shipid, quantity, label, description,' + \
                ' signature, capacity, handling, speed, (weapon_dmg_em + weapon_dmg_explosive + weapon_dmg_kinetic + weapon_dmg_thermal) AS weapon_power, weapon_turrets, weapon_tracking_speed, hull, shield, recycler_output, long_distance_capacity, droppods' + \
                ' FROM planet_ships LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id)' + \
                ' WHERE planetid=' + str(self.currentPlanetId) + \
                ' ORDER BY category, label'
        ships = dbRows(query)
        tpl.set('ships', ships)
        
        #---

        return Response(tpl.data)
