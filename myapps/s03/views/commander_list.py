# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
            
        #---
        
        dbQuery('SELECT sp_commanders_check_new_commanders(' + str(self.userId) + ')')

        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################

    def post(self, request, *args, **kwargs):
        
        #---

        action = request.POST.get('action')
        
        #---
        
        if action == 'rename':
        
            commanderId = ToInt(request.POST.get('id'), 0)
            newName = request.POST.get('name')            
            query = 'SELECT sp_commanders_rename(' + str(self.userId) + ',' + str(commanderId) + ',' + dosql(newName) + ')'
            dbQuery(query)            
        
        #---
        
        elif action == 'engage':
        
            commanderId = ToInt(request.POST.get('id'), 0)
            query = 'SELECT sp_commanders_engage(' + str(self.userId) + ',' + str(commanderId) + ')'
            dbQuery(query)
        
        #---
        
        elif action == 'train':
        
            commanderId = ToInt(request.POST.get('id'), 0)
            query = 'SELECT sp_commanders_train(' + str(self.userId) + ',' + str(commanderId) + ')'
            dbQuery(query)
        
        #---
        
        elif action == 'fire':
        
            commanderId = ToInt(request.POST.get('id'), 0)
            query = 'SELECT sp_commanders_fire(' + str(self.userId) + ',' + str(commanderId) + ')'
            dbQuery(query)

        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
        
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, 'commander-list')

        self.selectedMenu = 'commanders'
        
        #---
        
        result = dbExecute('SELECT int4(count(1)) FROM commanders WHERE recruited <= now() AND ownerid=' + str(self.userId))
        can_engage = result < self.profile['mod_commanders']
        tpl.set('can_engage', can_engage)
        
        tpl.set('max_commanders', int(self.profile['mod_commanders']))
        
        #---
        
        query = 'SELECT c.id AS cmd_id, c.name AS cmd_name, c.recruited, points, added, salary, can_be_fired, ' + \
                ' p.id AS planet_id, p.galaxy, p.sector, p.planet, p.name AS planet_name, ' + \
                ' f.id AS fleet_id, f.name AS fleet_name, ' + \
                ' c.mod_production_ore, c.mod_production_hydrocarbon, c.mod_production_energy, ' + \
                ' c.mod_production_workers, c.mod_fleet_speed, c.mod_fleet_shield, ' + \
                ' c.mod_fleet_handling, c.mod_fleet_tracking_speed, c.mod_fleet_damage, c.mod_fleet_signature, '  + \
                ' c.mod_construction_speed_buildings, c.mod_construction_speed_ships, last_training < now() - INTERVAL \'1 day\' AS can_train, sp_commanders_prestige_to_train(c.ownerid, c.id) AS train_cost, salary_increases >= 20 AS cant_train_anymore' + \
                ' FROM commanders AS c' + \
                '  LEFT JOIN fleets AS f ON (c.id=f.commanderid)' + \
                '  LEFT JOIN nav_planet AS p ON (c.id=p.commanderid)' + \
                ' WHERE c.recruited IS NOT NULL AND c.ownerid=' + str(self.userId) + \
                ' ORDER BY upper(c.name)'
        commanders = dbRows(query)
        tpl.set('commanders', commanders)
        
        for commander in commanders:
            
            commander['mod_production_ore'] = round((commander['mod_production_ore'] - 1.0) * 100)
            commander['mod_production_hydrocarbon'] = round((commander['mod_production_hydrocarbon'] - 1.0) * 100)
            commander['mod_production_energy'] = round((commander['mod_production_energy'] - 1.0) * 100)
            commander['mod_production_workers'] = round((commander['mod_production_workers'] - 1.0) * 100)

            commander['mod_fleet_speed'] = round((commander['mod_fleet_speed'] - 1.0) * 100)
            commander['mod_fleet_shield'] = round((commander['mod_fleet_shield'] - 1.0) * 100)
            commander['mod_fleet_handling'] = round((commander['mod_fleet_handling'] - 1.0) * 100)
            commander['mod_fleet_tracking_speed'] = round((commander['mod_fleet_tracking_speed'] - 1.0) * 100)
            commander['mod_fleet_damage'] = round((commander['mod_fleet_damage'] - 1.0) * 100)
            commander['mod_fleet_signature'] = round((commander['mod_fleet_signature'] - 1.0) * 100)

            commander['mod_construction_speed_buildings'] = round((commander['mod_construction_speed_buildings'] - 1.0) * 100)
            commander['mod_construction_speed_ships'] = round((commander['mod_construction_speed_ships'] - 1.0) * 100)
        
        #---
        
        query = 'SELECT c.id AS cmd_id, c.name AS cmd_name, points, added, salary,' + \
                ' c.mod_production_ore, c.mod_production_hydrocarbon, c.mod_production_energy, ' + \
                ' c.mod_production_workers, c.mod_fleet_speed, c.mod_fleet_shield, ' + \
                ' c.mod_fleet_handling, c.mod_fleet_tracking_speed, c.mod_fleet_damage, c.mod_fleet_signature, '  + \
                ' c.mod_construction_speed_buildings, c.mod_construction_speed_ships' + \
                ' FROM commanders AS c' + \
                ' WHERE c.recruited IS NULL AND c.ownerid=' + str(self.userId) + \
                ' ORDER BY upper(c.name)'
        available_commanders = dbRows(query)
        tpl.set('available_commanders', available_commanders)
        
        for commander in available_commanders:
            
            commander['mod_production_ore'] = round((commander['mod_production_ore'] - 1.0) * 100)
            commander['mod_production_hydrocarbon'] = round((commander['mod_production_hydrocarbon'] - 1.0) * 100)
            commander['mod_production_energy'] = round((commander['mod_production_energy'] - 1.0) * 100)
            commander['mod_production_workers'] = round((commander['mod_production_workers'] - 1.0) * 100)

            commander['mod_fleet_speed'] = round((commander['mod_fleet_speed'] - 1.0) * 100)
            commander['mod_fleet_shield'] = round((commander['mod_fleet_shield'] - 1.0) * 100)
            commander['mod_fleet_handling'] = round((commander['mod_fleet_handling'] - 1.0) * 100)
            commander['mod_fleet_tracking_speed'] = round((commander['mod_fleet_tracking_speed'] - 1.0) * 100)
            commander['mod_fleet_damage'] = round((commander['mod_fleet_damage'] - 1.0) * 100)
            commander['mod_fleet_signature'] = round((commander['mod_fleet_signature'] - 1.0) * 100)

            commander['mod_construction_speed_buildings'] = round((commander['mod_construction_speed_buildings'] - 1.0) * 100)
            commander['mod_construction_speed_ships'] = round((commander['mod_construction_speed_ships'] - 1.0) * 100)
        
        #---
        
        return self.display(tpl, request)
