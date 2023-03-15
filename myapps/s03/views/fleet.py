# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        self.fleetId = ToInt(request.GET.get("id"), 0)
        if self.fleetId == 0: return HttpResponseRedirect("/s03/fleets/")

        #---
        
        allianceId = -1
        if self.allianceId and self.hasRight("can_order_other_fleets"):
            allianceId = self.allianceId
            
        query = "SELECT ownerid" + \
                " FROM vw_fleets as f" + \
                " WHERE (ownerid=" + str(self.userId) + " OR (shared AND owner_alliance_id=" + str(allianceId) + ")) AND id=" + str(self.fleetId) + " AND (SELECT privilege FROM users WHERE users.id = f.ownerid) = 0"
        self.fleetOwnerId = dbExecute(query)
        if not self.fleetOwnerId: return HttpResponseRedirect("/s03/fleets/")
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        action = request.POST.get("action")
        
        #---
        
        if action == 'invade':
            
            take = request.POST.get("take", "") != ""
            droppods = ToInt(request.POST.get("droppods"), 0)
            
            result = dbExecute("SELECT sp_invade_planet(" + str(self.fleetOwnerId) + "," + str(self.fleetId) + "," + str(droppods) +"," + str(ToBool(take, False)) +")")            
            if result > 0: return HttpResponseRedirect("/s03/invasion/?id=" + str(result) + " +fleetid=" + str(self.fleetId))
            elif result == -1: messages.error(request, 'error_soldiers')
            elif result == -2: messages.error(request, 'error_fleet')
            elif result == -3: messages.error(request, 'error_planet')
            elif result == -5: messages.error(request, 'error_invade_enemy_ships')
            
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
            
        #---
        
        elif action == 'rename':
            
            newname = request.POST.get("newname").strip()
            
            if isValidObjectName(newname): dbQuery("UPDATE fleets SET name=" + dosql(newname) +" WHERE action=0 AND not engaged AND ownerid=" + str(self.userId) + " AND id=" + str(self.fleetId))
            else: messages.error(request, 'error_name')
            
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
            
        #---
        
        elif action == 'assigncommander':
        
            newcommanderid = ToInt(request.POST.get("commander"), 0)
            
            if newcommanderid != 0: dbExecute("SELECT sp_commanders_assign(" + str(self.userId) + "," + str(newcommanderid) + ",NULL," + str(self.fleetId) + ")")
            else: dbQuery("UPDATE fleets SET commanderid=null WHERE ownerid=" + str(self.userId) + " AND id=" + str(self.fleetId))
            
            dbExecute("SELECT sp_update_fleet_bonus(" + str(self.fleetId) + ")")
            
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
            
        #---
        
        elif action == 'move':
        
            g = ToInt(request.POST.get("g"), -1)
            s = ToInt(request.POST.get("s"), -1)
            p = ToInt(request.POST.get("p"), -1)
            
            if g == -1 or s == -1 or p == -1:
                messages.error(request, 'bad_destination')
                return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
            
            result = dbExecute("SELECT sp_move_fleet(" + str(self.fleetOwnerId) + "," + str(self.fleetId) + "," + str(g) + "," + str(s) + "," + str(p) + ")")
            if result == 0:
            
                movetype = request.POST.get("movetype")
                
                if movetype == "1": dbQuery("UPDATE fleets SET next_waypointid = sp_create_route_unload_move(planetid) WHERE ownerid=" + str(self.fleetOwnerId) + " AND id=" + str(self.fleetId))
                elif movetype == "2": dbQuery("UPDATE fleets SET next_waypointid = sp_create_route_recycle_move(planetid) WHERE ownerid=" + str(self.fleetOwnerId) + " AND id=" + str(self.fleetId))
            
            elif result == -4: messages.error(request, 'new_player_protection')
            elif result == -5: messages.error(request, 'long_travel_impossible')
            elif result == -6: messages.error(request, 'not_enough_credits')
            elif result == -7: messages.error(request, 'error_jump_from_require_empty_location')
            elif result == -8: messages.error(request, 'error_jump_protected_galaxy')
            elif result == -9: messages.error(request, 'error_jump_to_require_empty_location')
            elif result == -10: messages.error(request, 'error_jump_to_same_point_limit_reached')
            
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
            
        return HttpResponseRedirect('/s03/fleets/')
    
    def get(self, request, *args, **kwargs):
        
        action = request.GET.get("action")
        
        #---
        
        if action == 'share':
            dbQuery("UPDATE fleets SET shared=not shared WHERE ownerid=" + str(self.fleetOwnerId) + " AND id=" + str(self.fleetId))
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
        
        elif action == 'abandon':
            dbExecute("SELECT sp_abandon_fleet(" + str(self.userId) + "," + str(self.fleetId) + ")")
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
        
        elif action == 'attack':
            dbQuery("UPDATE fleets SET attackonsight=firepower > 0 WHERE ownerid=" + str(self.fleetOwnerId) + " AND id=" + str(self.fleetId))
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
        
        elif action == 'defend':
            dbQuery("UPDATE fleets SET attackonsight=False WHERE ownerid=" + str(self.fleetOwnerId) + " AND id=" + str(self.fleetId))
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
        
        elif action == 'recycle':
            result = dbExecute("SELECT sp_start_recycling(" + str(self.fleetOwnerId) + "," + str(self.fleetId) + ")")
            if result == -2: messages.error(request, 'error_recycling')
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
        
        elif action == "stoprecycling":
            dbExecute("SELECT sp_cancel_recycling(" + str(self.fleetOwnerId) + "," + str(self.fleetId) + ")")
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
            
        elif action == "stopwaiting":
            dbExecute("SELECT sp_cancel_waiting(" + str(self.fleetOwnerId) + "," + str(self.fleetId) + ")")
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
            
        elif action == "merge":
            destfleetid = ToInt(request.GET.get("with"), 0)
            dbExecute("SELECT sp_merge_fleets(" + str(self.userId) + "," + str(self.fleetId) + "," + str(destfleetid) +")")
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
            
        elif action == "return":
            dbExecute("SELECT sp_cancel_move(" + str(self.fleetOwnerId) + "," + str(self.fleetId) + ")")
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
            
        elif action == "install":
        
            shipid = ToInt(self.request.GET.get("s"), 0)
            
            result = oConnExecute("SELECT sp_start_ship_building_installation(" + str(self.fleetOwnerId) + "," + str(self.fleetId) + "," + str(shipid) + ")")
            if result >= 0: self.currentPlanetId = result
            elif result == -7: messages.error(request, 'error_max_planets_reached')
            elif result == -8: messages.error(request, 'error_deploy_enemy_ships')
            elif result == -11: messages.error(request, 'error_deploy_too_many_safe_planets')

            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
            
        elif action == "warp":
            dbExecute("SELECT sp_warp_fleet(" + str(self.fleetOwnerId) + "," + str(self.fleetId) + ")")
            return HttpResponseRedirect('/s03/fleet/?id=' + str(self.fleetId))
        
        #---
        
        content = getTemplate(self.request, "s03/fleet")
        
        self.selectedMenu = "fleets"

        #---
        
        query = "SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername," + \
                " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation," + \
                " destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_ownerid, destplanet_owner_name, destplanet_owner_relation," + \
                " cargo_capacity, cargo_load, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers," + \
                " recycler_output, orbit_ore, orbit_hydrocarbon, action, total_time, idle_time, date_part('epoch', const_interval_before_invasion()) AS before_invasion," + \
                " long_distance_capacity, droppods, warp_to," + \
                "( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.planet_galaxy AND nav_planet.sector = f.planet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = " + str(self.userId)+")) AS from_radarstrength, " + \
                "( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.destplanet_galaxy AND nav_planet.sector = f.destplanet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = " + str(self.userId)+")) AS to_radarstrength," + \
                "firepower, next_waypointid, (SELECT routeid FROM routes_waypoints WHERE id=f.next_waypointid) AS routeid, now(), spawn_ore, spawn_hydrocarbon," + \
                "radar_jamming, planet_floor, real_signature, required_vortex_strength, upkeep, CASE WHEN planet_owner_relation IN (-1,-2) THEN const_upkeep_ships_in_position() ELSE const_upkeep_ships() END AS upkeep_multiplicator," + \
                " ((sp_commander_fleet_bonus_efficiency(size::bigint - leadership, 2.0)-1.0)*100)::integer AS commander_efficiency, leadership, ownerid, shared," + \
                " (SELECT prestige_points >= sp_get_prestige_cost_for_new_planet(planets) FROM users WHERE id=ownerid) AS can_take_planet," + \
                " (SELECT sp_get_prestige_cost_for_new_planet(planets) FROM users WHERE id=ownerid) AS prestige_cost" + \
                " FROM vw_fleets as f" + \
                " WHERE ownerid=" + str(self.fleetOwnerId) + " AND id=" + str(self.fleetId)
        fleet = dbRow(query)
        if fleet == None: return HttpResponseRedirect("/s03/fleets/")
        content.setValue("fleet", fleet)

        #---

        if self.allianceId and fleet['shared']: content.Parse("shared")

        #---

        if fleet['action'] == -1 or fleet['action'] == 1:

            timelimit = int(100 / fleet['speed'] * 3600)
            if timelimit < 120: timelimit = 120

            if not fleet['engaged'] and fleet['total_time'] - fleet['remaining_time'] < timelimit and fleet['planetid']:
                content.setValue("timelimit", timelimit - (fleet['total_time'] - fleet['remaining_time']))
                content.Parse("can_cancel_moving")

        elif not fleet['engaged'] and fleet['action'] == 0:

            content.Parse("can_move")
            
            #---
            
            if fleet['warp_to']: content.Parse("can_warp")

            if fleet['recycler_output'] != 0 and (fleet['orbit_ore'] or fleet['orbit_hydrocarbon'] or fleet['spawn_ore'] or fleet['spawn_hydrocarbon']): content.Parse("can_recycle")

            if ((fleet['planet_ownerid'] == None) or (fleet['planet_owner_relation'] >= rHostile)) and (fleet['warp_to'] == None): content.Parse("can_install_building")
            
            if fleet['cargo_load'] > 0 and fleet['planet_owner_relation'] >= rFriend: content.Parse("can_unload_cargo")
            
            if fleet['cargo_capacity'] > 0 and fleet['planet_owner_relation'] == rSelf:
            
                content.Parse("can_load_cargo")
                
                query = "SELECT ore, hydrocarbon, scientists, soldiers," + \
                        " GREATEST(0, workers-GREATEST(workers_busy,workers_for_maintenance-workers_for_maintenance/2+1,500)) AS workers," + \
                        " workers > workers_for_maintenance/2" + \
                        " FROM vw_planets WHERE id=" + str(fleet['planetid'])
                planet = dbRow(query)
                content.setValue("planet", planet)
                
            if fleet['size'] > 1 and self.fleetOwnerId == self.userId:
            
                content.Parse("can_split")
                
                if fleet['planet_ownerid'] == self.userId: content.Parse("can_manage")

            if fleet['planet_ownerid'] and fleet['planet_owner_relation'] < rFriend and fleet['droppods'] > 0:

                content.Parse("can_invade")
            
                if fleet['idle_time'] < fleet['before_invasion']: t = fleet['before_invasion'] - fleet['idle_time']
                else: t = 0 
                content.setValue("invade_time", int(t))
            
            #---
            
            query = "SELECT id, name, galaxy, sector, planet FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.userId) + " ORDER BY id"
            planetgroup = dbRows(query)
            content.setValue("planetgroup", planetgroup)
            
            #---
            
            query = " SELECT DISTINCT ON (f.planetid) f.name, f.planetid, f.planet_galaxy, f.planet_sector, f.planet_planet" + \
                    " FROM vw_fleets AS f" + \
                    "  LEFT JOIN nav_planet AS p ON (f.planetid=p.id)" + \
                    " WHERE f.ownerid=" + str(self.userId)+" AND p.ownerid IS DISTINCT FROM " + str(self.userId) + \
                    " ORDER BY f.planetid" + \
                    " LIMIT 200"
            fleetgroup = dbRows(query)
            content.setValue("fleetgroup", fleetgroup)
            
            #---
            
            query = " SELECT id, galaxy, sector, planet" + \
                    " FROM nav_planet" + \
                    " WHERE ownerid=3"
            if fleet['planet_galaxy']: query = query + " AND galaxy=" + str(fleet['planet_galaxy'])
            query = query + " ORDER BY id"
            merchantplanetsgroup = dbRows(query)
            content.setValue("merchantplanetsgroup", merchantplanetsgroup)

        #---

        if fleet['routeid']:

            query = "SELECT routes_waypoints.id, ""action"", p.id, p.galaxy, p.sector, p.planet, p.name, sp_get_user(p.ownerid), sp_relation(p.ownerid," + str(self.userId)+") AS relation," + \
                    " routes_waypoints.ore, routes_waypoints.hydrocarbon" + \
                    " FROM routes_waypoints" + \
                    "    LEFT JOIN nav_planet AS p ON (routes_waypoints.planetid=p.id)" + \
                    " WHERE routeid=" + str(fleet['routeid']) + " AND routes_waypoints.id >= " + str(fleet['next_waypointid']) + \
                    " ORDER BY routes_waypoints.id"
            actions = dbRows(query)
            content.setValue("actions", actions)
        
        #---
        
        query = 'SELECT id, name, fleetname, planetname, fleetid ' + \
                ' FROM vw_commanders' + \
                ' WHERE ownerid=' + str(self.userId) + \
                ' ORDER BY fleetid IS NOT NULL, planetid IS NOT NULL, fleetid, planetid'
        commanders = dbRows(query)

        cmd_groups = []
        content.setValue('optgroups', cmd_groups)
        
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
        
            query = "SELECT vw_fleets.id, vw_fleets.name, size, signature, speed, cargo_load, cargo_capacity, action, ownerid, owner_name, alliances.tag, sp_relation(" + str(self.userId)+",ownerid) AS relation" + \
                    " FROM vw_fleets" + \
                    "    LEFT JOIN alliances ON alliances.id=owner_alliance_id" + \
                    " WHERE planetid=" + str(fleet['planetid'])+" AND vw_fleets.id != " + str(fleet['id'])+" AND NOT engaged AND action != 1 AND action != -1" + \
                    " ORDER BY upper(vw_fleets.name)"
            fleets = dbRows(query)
            content.setValue("fleets", fleets)
        
        #---
        
        query = "SELECT db_ships.id, fleets_ships.quantity, label, description," + \
                " signature, capacity, handling, speed, weapon_turrets, weapon_dmg_em+weapon_dmg_explosive+weapon_dmg_kinetic+weapon_dmg_thermal AS weapon_power, weapon_tracking_speed, hull, shield, recycler_output, long_distance_capacity, droppods," + \
                " buildingid, sp_can_build_on(" + str(fleet['planetid']) + ", db_ships.buildingid," + str(fleet['planet_ownerid']) + ")=0 AS can_build" + \
                " FROM fleets_ships" + \
                "    LEFT JOIN db_ships ON (fleets_ships.shipid = db_ships.id)" + \
                " WHERE fleetid=" + str(fleet['id']) + \
                " ORDER BY db_ships.category, db_ships.label"
        ships = dbRows(query)
        content.setValue("ships", ships)
        
        #---
        
        return self.display(content)
