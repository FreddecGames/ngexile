# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]
    
    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        self.fleetId = ToInt(request.GET.get('id'), 0)
        if self.fleetId == 0:
            return HttpResponseRedirect('/s03/')

        #---
        
        allianceId = -1
        if self.allianceId and self.hasRight('can_order_other_fleets'):
            allianceId = self.allianceId
            
        query = 'SELECT ownerid' + \
                ' FROM vw_fleets as f' + \
                ' WHERE (ownerid=' + str(self.userId) + ' OR (shared AND owner_alliance_id=' + str(allianceId) + ')) AND id=' + str(self.fleetId) + ' AND (SELECT privilege FROM users WHERE users.id = f.ownerid) = 0'
        self.fleetOwnerId = dbExecute(query)
        
        if not self.fleetOwnerId:
            return HttpResponseRedirect('/s03/')
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'invade':
            
            take = request.POST.get('take', '') != ''
            droppods = ToInt(request.POST.get('droppods'), 0)
            
            result = dbExecute('SELECT sp_invade_planet(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ',' + str(droppods) +',' + str(ToBool(take, False)) +')')            
            if result > 0: return HttpResponseRedirect('/s03/report-invasion/?id=' + str(result) + '&fleetid=' + str(self.fleetId))
            elif result == -1: messages.error(request, 'error_soldiers')
            elif result == -2: messages.error(request, 'error_fleet')
            elif result == -3: messages.error(request, 'error_planet')
            elif result == -5: messages.error(request, 'error_invade_enemy_ships')
            
        #---
        
        elif action == 'rename':
            
            newname = request.POST.get('newname').strip()
            
            if isValidObjectName(newname): dbQuery('UPDATE fleets SET name=' + dosql(newname) +' WHERE action=0 AND not engaged AND ownerid=' + str(self.userId) + ' AND id=' + str(self.fleetId))
            else: messages.error(request, 'error_name')
            
        #---
        
        elif action == 'assigncommander':
        
            newcommanderid = ToInt(request.POST.get('commander'), 0)
            
            if newcommanderid != 0: dbQuery('SELECT sp_commanders_assign(' + str(self.userId) + ',' + str(newcommanderid) + ',NULL,' + str(self.fleetId) + ')')
            else: dbQuery('UPDATE fleets SET commanderid=null WHERE ownerid=' + str(self.userId) + ' AND id=' + str(self.fleetId))
            
            dbQuery('SELECT sp_update_fleet_bonus(' + str(self.fleetId) + ')')
            
        #---
        
        elif action == 'move':
        
            g = ToInt(request.POST.get('g'), -1)
            s = ToInt(request.POST.get('s'), -1)
            p = ToInt(request.POST.get('p'), -1)
            
            if g == -1 or s == -1 or p == -1:
                messages.error(request, 'bad_destination')
                return HttpResponseRedirect('/s03/fleet-view/?id=' + str(self.fleetId))
            
            result = dbExecute('SELECT sp_move_fleet(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ',' + str(g) + ',' + str(s) + ',' + str(p) + ')')
            if result == 0:
            
                movetype = request.POST.get('movetype')
                
                if movetype == '1': dbQuery('UPDATE fleets SET next_waypointid = sp_create_route_unload_move(planetid) WHERE ownerid=' + str(self.fleetOwnerId) + ' AND id=' + str(self.fleetId))
                elif movetype == '2': dbQuery('UPDATE fleets SET next_waypointid = sp_create_route_recycle_move(planetid) WHERE ownerid=' + str(self.fleetOwnerId) + ' AND id=' + str(self.fleetId))
            
            elif result == -4: messages.error(request, 'new_player_protection')
            elif result == -5: messages.error(request, 'long_travel_impossible')
            elif result == -6: messages.error(request, 'not_enough_credits')
            elif result == -7: messages.error(request, 'error_jump_from_require_empty_location')
            elif result == -8: messages.error(request, 'error_jump_protected_galaxy')
            elif result == -9: messages.error(request, 'error_jump_to_require_empty_location')
            elif result == -10: messages.error(request, 'error_jump_to_same_point_limit_reached')
            
        #---
        
        elif action == 'transfer':
        
            ore = ToInt(request.POST.get('load_ore'), 0) - ToInt(request.POST.get('unload_ore'), 0)
            hydrocarbon = ToInt(request.POST.get('load_hydrocarbon'), 0) - ToInt(request.POST.get('unload_hydrocarbon'), 0)
            scientists = ToInt(request.POST.get('load_scientists'), 0) - ToInt(request.POST.get('unload_scientists'), 0)
            soldiers = ToInt(request.POST.get('load_soldiers'), 0) - ToInt(request.POST.get('unload_soldiers'), 0)
            workers = ToInt(request.POST.get('load_workers'), 0) - ToInt(request.POST.get('unload_workers'), 0)
        
            if ore != 0 or hydrocarbon != 0 or scientists != 0 or soldiers != 0 or workers != 0:
                dbQuery('SELECT sp_transfer_resources_with_planet(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ',' + str(ore) + ',' + str(hydrocarbon) + ',' + str(scientists) + ',' + str(soldiers) + ',' + str(workers) + ')')
        
        #---
        
        if action == 'share':
            dbQuery('UPDATE fleets SET shared=not shared WHERE ownerid=' + str(self.fleetOwnerId) + ' AND id=' + str(self.fleetId))
        
        #---
        
        elif action == 'abandon':
            dbQuery('SELECT sp_abandon_fleet(' + str(self.userId) + ',' + str(self.fleetId) + ')')
        
        #---
        
        elif action == 'attack':
            dbQuery('UPDATE fleets SET attackonsight=firepower > 0 WHERE ownerid=' + str(self.fleetOwnerId) + ' AND id=' + str(self.fleetId))
        
        #---
        
        elif action == 'defend':
            dbQuery('UPDATE fleets SET attackonsight=False WHERE ownerid=' + str(self.fleetOwnerId) + ' AND id=' + str(self.fleetId))
        
        #---
        
        elif action == 'recycle':
            result = dbExecute('SELECT sp_start_recycling(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ')')
            if result == -2: messages.error(request, 'error_recycling')
        
        #---
        
        elif action == 'stoprecycling':
            dbQuery('SELECT sp_cancel_recycling(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ')')
        
        #---
            
        elif action == 'stopwaiting':
        
            dbQuery('SELECT sp_cancel_waiting(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ')')
        
        #---
            
        elif action == 'merge':
        
            destfleetid = ToInt(request.POST.get('with'), 0)
            dbQuery('SELECT sp_merge_fleets(' + str(self.userId) + ',' + str(self.fleetId) + ',' + str(destfleetid) +')')
            
        #---
            
        elif action == 'return':
            dbQuery('SELECT sp_cancel_move(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ')')
        
        #---
            
        elif action == 'install':
        
            shipid = ToInt(request.POST.get('s'), 0)
            
            result = dbExecute('SELECT sp_start_ship_building_installation(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ',' + str(shipid) + ')')
            if result >= 0: self.currentPlanetId = result
            elif result == -7: messages.error(request, 'error_max_planets_reached')
            elif result == -8: messages.error(request, 'error_deploy_enemy_ships')
            elif result == -11: messages.error(request, 'error_deploy_too_many_safe_planets')
        
        #---
            
        elif action == 'warp':
            dbQuery('SELECT sp_warp_fleet(' + str(self.fleetOwnerId) + ',' + str(self.fleetId) + ')')
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate()
                
        #---
        
        query = 'SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername,' + \
                ' planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation,' + \
                ' destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_ownerid, destplanet_owner_name, destplanet_owner_relation,' + \
                ' cargo_capacity, cargo_load, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers,' + \
                ' recycler_output, orbit_ore, orbit_hydrocarbon, action, total_time, idle_time, date_part(\'epoch\', const_interval_before_invasion()) AS before_invasion,' + \
                ' long_distance_capacity, droppods, warp_to,' + \
                '( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.planet_galaxy AND nav_planet.sector = f.planet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = ' + str(self.userId) + ')) AS from_radarstrength, ' + \
                '( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.destplanet_galaxy AND nav_planet.sector = f.destplanet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = ' + str(self.userId) + ')) AS to_radarstrength,' + \
                'firepower, next_waypointid, (SELECT routeid FROM routes_waypoints WHERE id=f.next_waypointid) AS routeid, now(), spawn_ore, spawn_hydrocarbon,' + \
                'radar_jamming, planet_floor, real_signature, required_vortex_strength, upkeep, CASE WHEN planet_owner_relation IN (-1,-2) THEN const_upkeep_ships_in_position() ELSE const_upkeep_ships() END AS upkeep_multiplicator,' + \
                ' ((sp_commander_fleet_bonus_efficiency(size::bigint - leadership, 2.0)-1.0)*100)::integer AS commander_efficiency, leadership, ownerid, shared,' + \
                ' (SELECT prestige_points >= sp_get_prestige_cost_for_new_planet(planets) FROM users WHERE id=ownerid) AS can_take_planet,' + \
                ' (SELECT sp_get_prestige_cost_for_new_planet(planets) FROM users WHERE id=ownerid) AS prestige_cost' + \
                ' FROM vw_fleets as f' + \
                ' WHERE ownerid=' + str(self.fleetOwnerId) + ' AND id=' + str(self.fleetId)
        fleet = dbRow(query)

        tpl.set('fleet', fleet)

        #---

        if self.allianceId and fleet['shared']: tpl.set('shared')

        #---

        if fleet['action'] == -1 or fleet['action'] == 1:

            timelimit = int(100 / fleet['speed'] * 3600)
            if timelimit < 120: timelimit = 120

            if not fleet['engaged'] and fleet['total_time'] - fleet['remaining_time'] < timelimit and fleet['planetid']:
                tpl.set('timelimit', timelimit - (fleet['total_time'] - fleet['remaining_time']))
                tpl.set('can_cancel_moving')

        elif not fleet['engaged'] and fleet['action'] == 0:

            tpl.set('can_move')
            
            #---
            
            if fleet['warp_to']: tpl.set('can_warp')
            
            if fleet['recycler_output'] > 0 and (fleet['orbit_ore'] or fleet['orbit_hydrocarbon'] or fleet['spawn_ore'] or fleet['spawn_hydrocarbon']): tpl.set('can_recycle')

            if ((fleet['planet_ownerid'] == None) or (fleet['planet_owner_relation'] >= rHostile)) and (fleet['warp_to'] == None): tpl.set('can_install_building')
            
            if fleet['cargo_load'] > 0 and fleet['planet_owner_relation'] >= rFriend: tpl.set('can_unload_cargo')
            
            if fleet['cargo_capacity'] > 0 and fleet['planet_owner_relation'] == rSelf:
            
                tpl.set('can_load_cargo')
                
                query = 'SELECT ore, hydrocarbon, scientists, soldiers,' + \
                        ' GREATEST(0, workers-GREATEST(workers_busy,workers_for_maintenance-workers_for_maintenance/2+1,500)) AS workers,' + \
                        ' workers > workers_for_maintenance/2' + \
                        ' FROM vw_planets WHERE id=' + str(fleet['planetid'])
                planet = dbRow(query)
                tpl.set('planet', planet)
                
            if fleet['planet_ownerid'] == self.userId: tpl.set('can_manage')
                
            if fleet['size'] > 1 and self.fleetOwnerId == self.userId: tpl.set('can_split')                

            if fleet['planet_ownerid'] and fleet['planet_owner_relation'] < rFriend and fleet['droppods'] > 0:

                tpl.set('can_invade')
            
                if fleet['idle_time'] < fleet['before_invasion']: t = fleet['before_invasion'] - fleet['idle_time']
                else: t = 0 
                tpl.set('invade_time', int(t))
            
            #---
            
            query = 'SELECT id, name, galaxy, sector, planet FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.userId) + ' ORDER BY id'
            planetgroup = dbRows(query)
            tpl.set('planetgroup', planetgroup)
            
            #---
            
            query = ' SELECT DISTINCT ON (f.planetid) f.name, f.planetid, f.planet_galaxy, f.planet_sector, f.planet_planet' + \
                    ' FROM vw_fleets AS f' + \
                    '  LEFT JOIN nav_planet AS p ON (f.planetid=p.id)' + \
                    ' WHERE f.ownerid=' + str(self.userId) + ' AND p.ownerid IS DISTINCT FROM ' + str(self.userId) + \
                    ' ORDER BY f.planetid' + \
                    ' LIMIT 200'
            fleetgroup = dbRows(query)
            tpl.set('fleetgroup', fleetgroup)
            
            #---
            
            query = ' SELECT id, galaxy, sector, planet' + \
                    ' FROM nav_planet' + \
                    ' WHERE ownerid=3'
            if fleet['planet_galaxy']: query = query + ' AND galaxy=' + str(fleet['planet_galaxy'])
            query = query + ' ORDER BY id'
            merchantplanetsgroup = dbRows(query)
            tpl.set('merchantplanetsgroup', merchantplanetsgroup)

        #---

        if fleet['routeid']:

            query = 'SELECT routes_waypoints.id, ''action'', p.id, p.galaxy, p.sector, p.planet, p.name, sp_get_user(p.ownerid), sp_relation(p.ownerid,' + str(self.userId) + ') AS relation,' + \
                    ' routes_waypoints.ore, routes_waypoints.hydrocarbon' + \
                    ' FROM routes_waypoints' + \
                    '    LEFT JOIN nav_planet AS p ON (routes_waypoints.planetid=p.id)' + \
                    ' WHERE routeid=' + str(fleet['routeid']) + ' AND routes_waypoints.id >= ' + str(fleet['next_waypointid']) + \
                    ' ORDER BY routes_waypoints.id'
            actions = dbRows(query)
            tpl.set('actions', actions)
        
        #---
        
        query = 'SELECT id, name, fleetname, planetname, fleetid ' + \
                ' FROM vw_commanders' + \
                ' WHERE ownerid=' + str(self.userId) + \
                ' ORDER BY fleetid IS NOT NULL, planetid IS NOT NULL, fleetid, planetid'
        commanders = dbRows(query)

        cmd_groups = []
        tpl.set('optgroups', cmd_groups)
        
        cmd_nones = { 'typ':'none', 'cmds':[] }
        cmd_fleets = { 'typ':'fleet', 'cmds':[] }
        cmd_planets = { 'typ':'planet', 'cmds':[] }
        
        for cmd in commanders:

            if cmd['fleetname'] == None and cmd['planetname'] == None:
                cmd_nones['cmds'].append(cmd)
                
            elif cmd['fleetname'] == None:
                cmd_planets['cmds'].append(cmd)
                
            else:
                cmd_fleets['cmds'].append(cmd)
                activity = dbRow('SELECT dest_planetid, engaged, action FROM fleets WHERE ownerid=' + str(self.userId)+' AND id=' + str(cmd['fleetid']))
                if not (activity['dest_planetid'] == None and not activity['engaged'] and activity['action'] == 0):
                    cmd['unavailable'] = True

        if len(cmd_nones['cmds']) > 0: cmd_groups.append(cmd_nones)
        if len(cmd_fleets['cmds']) > 0: cmd_groups.append(cmd_fleets)
        if len(cmd_planets['cmds']) > 0: cmd_groups.append(cmd_planets)        
        
        #---
        
        if fleet['action'] != -1 and fleet['planetid']:
        
            query = 'SELECT vw_fleets.id, vw_fleets.name, size, signature, speed, cargo_load, cargo_capacity, action, ownerid, owner_name, alliances.tag, sp_relation(' + str(self.userId) + ',ownerid) AS relation' + \
                    ' FROM vw_fleets' + \
                    '    LEFT JOIN alliances ON alliances.id=owner_alliance_id' + \
                    ' WHERE planetid=' + str(fleet['planetid']) + ' AND vw_fleets.id != ' + str(fleet['id']) + ' AND NOT engaged AND action != 1 AND action != -1' + \
                    ' ORDER BY upper(vw_fleets.name)'
            fleets = dbRows(query)
            tpl.set('fleets', fleets)
        
        #---
        
        if fleet['planet_ownerid']: planet_ownerid = fleet['planet_ownerid']
        else: planet_ownerid = self.userId

        query = 'SELECT db_ships.id, fleets_ships.quantity, label, description,' + \
                ' signature, capacity, handling, speed, weapon_turrets, weapon_dmg_em+weapon_dmg_explosive+weapon_dmg_kinetic+weapon_dmg_thermal AS weapon_power, weapon_tracking_speed, hull, shield, recycler_output, long_distance_capacity, droppods,' + \
                ' buildingid, sp_can_build_on(' + str(fleet['planetid']) + ', db_ships.buildingid,' + str(planet_ownerid) + ')=0 AS can_build' + \
                ' FROM fleets_ships' + \
                '    LEFT JOIN db_ships ON (fleets_ships.shipid = db_ships.id)' + \
                ' WHERE fleetid=' + str(fleet['id']) + \
                ' ORDER BY db_ships.category, db_ships.label'
        ships = dbRows(query)
        tpl.set('ships', ships)
        
        #---
        
        if fleet['action'] == 0 and fleet['planet_owner_relation'] == rSelf:
        
            self.showHeader = True
            self.headerUrl = '/s03/planet-orbit/'
        
            self.currentPlanetId = fleet['planetid']
            
        #---
        
        return Response(tpl.data)
