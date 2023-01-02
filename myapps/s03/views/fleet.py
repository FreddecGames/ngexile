# -*- coding: utf-8 -*-

from ._global import *

from .accounts import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        self.selected_menu = "fleets.fleets"

        self.action_result = ""
        self.move_fleet_result = ""
        self.can_command_alliance_fleets = -1
        self.can_install_building = False

        if self.AllianceId and self.hasRight("can_order_other_fleets"):
            self.can_command_alliance_fleets = self.AllianceId

        self.fleet_owner_id = self.UserId

        fleetid = ToInt(self.request.GET.get("id"), 0)

        if ToInt(self.request.GET.get("trade", ""), 0) == 9:
            self.action_result = "error_trade"

        if fleetid == 0:
            return HttpResponseRedirect("/s03/orbit/")

        self.RetrieveFleetOwnerId(fleetid)

        response = self.ExecuteOrder(fleetid)
        if response: return response

        return self.DisplayFleet(fleetid)

    def RetrieveFleetOwnerId(self, fleetid):

        # retrieve fleet owner
        query = "SELECT ownerid" + \
                " FROM vw_fleets as f" + \
                " WHERE (ownerid=" + str(self.UserId) + " OR (shared AND owner_alliance_id=" + str(self.can_command_alliance_fleets) + ")) AND id=" + str(fleetid) + " AND (SELECT privilege FROM users WHERE users.id = f.ownerid) = 0"
        oRs = oConnExecute(query)

        if oRs:
            self.fleet_owner_id = oRs[0]

    # display fleet info
    def DisplayFleet(self, fleetid):

        content = GetTemplate(self.request, "fleet")

        # retrieve fleet name, size, position, destination
        query = "SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername," + \
                " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation," + \
                " destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_ownerid, destplanet_owner_name, destplanet_owner_relation," + \
                " cargo_capacity, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers," + \
                " recycler_output, orbit_ore > 0 OR orbit_hydrocarbon > 0, action, total_time, idle_time, date_part('epoch', const_interval_before_invasion())," + \
                " long_distance_capacity, droppods, warp_to,"+ \
                "( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.planet_galaxy AND nav_planet.sector = f.planet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = "+str(self.UserId)+")) AS from_radarstrength, " + \
                "( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.destplanet_galaxy AND nav_planet.sector = f.destplanet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = "+str(self.UserId)+")) AS to_radarstrength," + \
                "firepower > 0, next_waypointid, (SELECT routeid FROM routes_waypoints WHERE id=f.next_waypointid), now(), spawn_ore + spawn_hydrocarbon," + \
                "radar_jamming, planet_floor, real_signature, required_vortex_strength, upkeep, CASE WHEN planet_owner_relation IN (-1,-2) THEN const_upkeep_ships_in_position() ELSE const_upkeep_ships() END AS upkeep_multiplicator," + \
                " ((sp_commander_fleet_bonus_efficiency(size::bigint - leadership, 2.0)-1.0)*100)::integer AS commander_efficiency, leadership, ownerid, shared," + \
                " (SELECT prestige_points >= sp_get_prestige_cost_for_new_planet(planets) FROM users WHERE id=ownerid) AS can_take_planet," + \
                " (SELECT sp_get_prestige_cost_for_new_planet(planets) FROM users WHERE id=ownerid) AS prestige_cost" + \
                " FROM vw_fleets as f" + \
                " WHERE ownerid=" + str(self.fleet_owner_id) + " AND id=" + str(fleetid)
        oRs = oConnExecute(query)

        # if fleet doesnt exist, redirect to the last known planet orbit or display the fleets list
        if oRs == None:
            return HttpResponseRedirect("/s03/fleets/")

        if self.AllianceId:
            if oRs[57]:
                content.Parse("shared")
            else:
                content.Parse("not_shared")
            
        content.AssignValue("now", oRs[46])

        if oRs[45]:

            query = "SELECT routes_waypoints.id, ""action"", p.id, p.galaxy, p.sector, p.planet, p.name, sp_get_user(p.ownerid), sp_relation(p.ownerid,"+str(self.UserId)+")," + \
                    " routes_waypoints.ore, routes_waypoints.hydrocarbon" + \
                    " FROM routes_waypoints" + \
                    "    LEFT JOIN nav_planet AS p ON (routes_waypoints.planetid=p.id)" + \
                    " WHERE routeid=" + str(oRs[45]) + " AND routes_waypoints.id >= " + str(oRs[44]) + \
                    " ORDER BY routes_waypoints.id"
            RouteRss = oConnExecuteAll(query)
            
            actions = []
            
            waypointscount = 0
            for RouteRs in RouteRss:
                action = {}
                if RouteRs[2]:
                    action["planetid"] = RouteRs[2]
                    action["g"] = RouteRs[3]
                    action["s"] = RouteRs[4]
                    action["p"] = RouteRs[5]
                    action["relation"] = RouteRs[8]

                    if RouteRs[8] >= rAlliance:
                        action["planetname"] = RouteRs[6]
                    elif RouteRs[8] >= rUninhabited:
                        action["planetname"] = RouteRs[7]
                    else:
                        action["planetname"] = ""

                if RouteRs[1] == 0:
                    if RouteRs[9] > 0:
                        action["loadall"] = True
                    else:
                        action["unloadall"] = True
                        
                elif RouteRs[1] == 1:
                    action["move"] = True
                elif RouteRs[1] == 2:
                    action["recycle"] = True
                elif RouteRs[1] == 4:
                    action["wait"] = True
                elif RouteRs[1] == 5:
                    action["invade"] = True

                actions.append(action)

                waypointscount = waypointscount + 1

            if waypointscount > 0: content.AssignValue("actions", actions)

        #
        # list commmanders
        #
        query = " SELECT c.id, c.name, c.fleetname, c.planetname, fleets.id AS available" + \
                " FROM vw_commanders AS c" + \
                "    LEFT JOIN fleets ON (c.fleetid=fleets.id AND c.ownerid=fleets.ownerid AND NOT engaged AND action=0)" + \
                " WHERE c.ownerid=" + str(self.fleet_owner_id) + \
                " ORDER BY c.fleetid IS NOT NULL, c.planetid IS NOT NULL, c.fleetid, c.planetid "
        oCmdListRss = oConnExecuteAll(query)

        lastItem = ""
        item = ""
        ShowGroup = True

        optgroup_none = {'none':True, 'cmd_options':[]}
        optgroup_fleet = {'fleet':True, 'cmd_options':[]}
        optgroup_planet = {'planet':True, 'cmd_options':[]}
        
        for oCmdListRs in oCmdListRss:
            cmd = {}
            if oCmdListRs[2] == None:
                if oCmdListRs[3] == None:
                    item = "none"
                    optgroup_none['cmd_options'].append(cmd)
                else:
                    item = "planet"
                    optgroup_planet['cmd_options'].append(cmd)
            else:
                item = "fleet"
                optgroup_fleet['cmd_options'].append(cmd)

            if item != lastItem:
                if ShowGroup: content.Parse("optgroup")
                content.Parse("optgroup."+item)
            
            # check if the commander is the commander of the fleet we display
            if oRs[8] == oCmdListRs[0]: cmd["selected"] = True

            cmd["cmd_id"] = oCmdListRs[0]
            cmd["cmd_name"] = oCmdListRs[1]

            if item == "planet": 
                cmd["name"] = oCmdListRs[3]
                cmd["assigned"] = True
            elif item == "fleet":
                cmd["name"] = oCmdListRs[2]

                if oCmdListRs[4]:
                    cmd["assigned"] = True
                else:
                    cmd["unavailable"] = True

            content.Parse("optgroup.cmd_option")
            ShowGroup = True
        if ShowGroup: content.Parse("optgroup")

        optgroups = []
        if len(optgroup_none['cmd_options']) > 0: optgroups.append(optgroup_none)
        if len(optgroup_fleet['cmd_options']) > 0: optgroups.append(optgroup_fleet)
        if len(optgroup_planet['cmd_options']) > 0: optgroups.append(optgroup_planet)
        content.AssignValue("optgroups", optgroups)
        
        if oRs[8] == None: # display "no commander" or "fire commander" in the combobox of commanders
            content.Parse("none")
            content.Parse("nocommander")
        else:
            content.Parse("unassigncommander")

            content.AssignValue("commanderid", oRs[8])
            content.AssignValue("commandername", oRs[9])
            content.Parse("commander")

        content.AssignValue("fleet_leadership", oRs[55])
        content.AssignValue("fleet_commander_efficiency", oRs[54])
        content.AssignValue("fleet_signature", oRs[5])
        content.AssignValue("fleet_real_signature", oRs[50])
        content.AssignValue("fleet_upkeep", oRs[52])
        content.AssignValue("fleet_upkeep_multiplicator", oRs[53])
        content.AssignValue("fleet_long_distance_capacity", oRs[38])
        content.AssignValue("fleet_required_vortex_strength", oRs[51])
        content.AssignValue("fleet_droppods", oRs[39])

        if oRs[39] <= 0: content.Parse("hide_droppods")

        if oRs[38] < oRs[50]: content.Parse("insufficient_long_distance_capacity")

        # display resources in cargo and its capacity
        content.AssignValue("fleet_ore", oRs[27])
        content.AssignValue("fleet_hydrocarbon", oRs[28])
        content.AssignValue("fleet_scientists", oRs[29])
        content.AssignValue("fleet_soldiers", oRs[30])
        content.AssignValue("fleet_workers", oRs[31])

        content.AssignValue("fleet_load", oRs[27] + oRs[28] + oRs[29] + oRs[30] + oRs[31])
        content.AssignValue("fleet_capacity", oRs[26])

        if oRs[26] <= 0:
            content.Parse("hide_cargo")

        content.AssignValue("fleetid", fleetid)
        content.AssignValue("fleetname", oRs[1])
        content.AssignValue("fleet_size", oRs[4])
        content.AssignValue("fleet_speed", oRs[6])
        content.AssignValue("recycler_output", oRs[32])

        if oRs[32] <= 0: content.Parse("hide_recycling")

        # Assign remaining time
        if oRs[7]:
            content.AssignValue("time", oRs[7])
        else:
            content.AssignValue("time", 0)

        #
        # display the fleet stance
        #
        if oRs[2]:
            content.Parse("attack")
        else:
            content.Parse("defend")

        # if the fleet can be set to attack (firepower > 0)
        if oRs[43]:
            if oRs[2]:
                content.Parse("setstance_defend")
            else:
                content.Parse("setstance_attack")

            content.Parse("setstance")
        else:
            content.Parse("cant_setstance")

        #
        # display fleets that are near the same planet as this fleet
        # it allows to switch between the fleets and merge them quickly
        #
        
        fleets = []
        
        fleetCount = 0
        if oRs[34] != -1 and oRs[10]:
            query = "SELECT vw_fleets.id, vw_fleets.name, size, signature, speed, cargo_capacity-cargo_free, cargo_capacity, action, ownerid, owner_name, alliances.tag, sp_relation("+str(self.UserId)+",ownerid)" + \
                    " FROM vw_fleets" + \
                    "    LEFT JOIN alliances ON alliances.id=owner_alliance_id" + \
                    " WHERE planetid="+str(oRs[10])+" AND vw_fleets.id != "+str(oRs[0])+" AND NOT engaged AND action != 1 AND action != -1" + \
                    " ORDER BY upper(vw_fleets.name)"
            oFleetsRss = oConnExecuteAll(query)

            for oFleetsRs in oFleetsRss:
                fleet = {}
            
                fleet["id"] = oFleetsRs[0]
                fleet["name"] = oFleetsRs[1]
                fleet["size"] = oFleetsRs[2]

                # oRs[48) radar_jamming of planet
                if oRs[17] > rFriend or oFleetsRs[11] > rFriend or oRs[48] == 0 or oRs[41] > oRs[48]:
                    fleet["signature"] = oFleetsRs[3]
                else:
                    fleet["signature"] = 0

                fleet["speed"] = oFleetsRs[4]
                fleet["cargo_load"] = oFleetsRs[5]
                fleet["cargo_capacity"] = oFleetsRs[6]

                if oFleetsRs[8] == self.UserId:
                    if oRs[34] == 0 and oFleetsRs[7] == 0: fleet["merge"] = True

                    fleet["playerfleet"] = True
                    
                    fleets.append(fleet)
                    fleetCount = fleetCount + 1
                else:
                    displayFleet = False

                    fleet["owner"] = oFleetsRs[9]
                    fleet["tag"] = oFleetsRs[10]

                    if oFleetsRs[11] == 1:
                        displayFleet = True
                        fleet["ally"] = True
                    elif oFleetsRs[11] == 0:
                        displayFleet = True
                        fleet["friend"] = True
                    elif oFleetsRs[11] == -1:
                        displayFleet = oRs[34] != 1
                        if displayFleet: fleet["enemy"] = True

                    # only display ally/nap fleets when leaving a planet
                    if displayFleet:
                        fleets.append(fleet)
                        fleetCount = fleetCount + 1

        if fleetCount == 0: content.Parse("nofleets")
        else: content.AssignValue("fleets", fleets)

        #
        # assign fleet current planet
        #
        content.AssignValue("planetid", oRs[10])
        content.AssignValue("g", oRs[12])
        content.AssignValue("s", oRs[13])
        content.AssignValue("p", oRs[14])
        content.AssignValue("relation", oRs[17])
        content.AssignValue("planetname", self.getPlanetName(oRs[17], oRs[41], oRs[16], oRs[11]))
        
        if oRs[34] == -1 or oRs[34] == 1: # fleet is moving when dest_planetid is not None

            # Assign destination planet
            content.AssignValue("t_planetid", oRs[18])
            content.AssignValue("t_g", oRs[20])
            content.AssignValue("t_s", oRs[21])
            content.AssignValue("t_p", oRs[22])
            content.AssignValue("t_relation", oRs[25])
            content.AssignValue("t_planetname", self.getPlanetName(oRs[25], oRs[42], oRs[24], oRs[19]))

            # display Cancel Move orders if fleet has covered less than 100 units of distance, or during 2 minutes
            # and if from_planet is not None
            timelimit = int(100/oRs[6]*3600)
            if timelimit < 120: timelimit = 120

            if not oRs[3] and oRs[35]-oRs[7] < timelimit and oRs[10]:
                content.AssignValue("timelimit", timelimit-(oRs[35]-oRs[7]))
                content.Parse("cancel_moving")

            if oRs[10]: content.Parse("from")

            content.Parse("moving")
        else:
            if oRs[3]: #if is engaged
                content.Parse("fighting")
            elif oRs[34] == 2:
                content.Parse("recycling")
            elif oRs[34] == 4:
                content.Parse("waiting")
            else:

                if oRs[40]: content.Parse("warp")

                if oRs[32] == 0 or (not oRs[33] and oRs[47] == 0): # if no recycler or nothing to recycle
                    content.Parse("cant_recycle")
                else:
                    content.Parse("recycle")

                self.can_install_building = ((oRs[15] == None) or (oRs[17] >= rHostile)) and (oRs[40] == None)

                # assign buildings that can be installed
                # only possible if not moving, not engaged, planet is owned by self or by nobody and is not a vortex

                if oRs[17] >= rFriend:
                    content.Parse("unloadcargo")

                if oRs[17] == rSelf and oRs[49] > 0:
                    content.Parse("loadcargo")
                    content.Parse("manage")

                if oRs[34] == 0 and oRs[4] > 1 and self.fleet_owner_id == self.UserId:
                    content.Parse("split")

                if oRs[15] and oRs[17] < rFriend and oRs[30] > 0:
                    # fleet has to wait some time (defined in DB) before being able to invade
                    # oRs[37] is the value returned by const_seconds_before_invasion() from DB
                    if oRs[36] < oRs[37]: t = oRs[37] - oRs[36]
                    else: t = 0 
                    content.AssignValue("invade_time", int(t))

                    if oRs[39] == 0:
                        content.Parse("cant_invade")
                    else:
                        if oRs[58]:
                            content.AssignValue("prestige", oRs[59])
                            content.Parse("can_take")

                        content.Parse("invade")
                    
                else:
                    content.Parse("cant_invade")

                if oRs[34] == 0:
                    content.Parse("patrolling") # standing by/patrolling
                    content.Parse("idle")

            #
            # Fleet idling
            #
            if oRs[34] == 0:
                if self.move_fleet_result != "":
                    content.Parse(self.move_fleet_result)
                    content.Parse("result")
                
                #
                # populate destination list, there are 2 groups : planets and fleets
                #

                # retrieve planet list
                index = 0
                hasAPlanetSelected = False

                planetListArray = checkPlanetListCache(self.request.session)
                if planetListArray:
                    planetgroup = []
                    for i in planetListArray:
                        planet = {}
                        
                        planet["index"] = index
                        planet["name"] = i[1]
                        planet["to_g"] = i[2]
                        planet["to_s"] = i[3]
                        planet["to_p"] = i[4]

                        if i[0] == oRs[10]:
                            planet["selected"] = True
                            hasAPlanetSelected = True

                        planetgroup.append(planet)
                        index += 1
                        
                    content.AssignValue("planetgroup", planetgroup)

                #
                # list planets where we have fleets not on our planets
                #
                query = " SELECT DISTINCT ON (f.planetid) f.name, f.planetid, f.planet_galaxy, f.planet_sector, f.planet_planet" + \
                        " FROM vw_fleets AS f" + \
                        "     LEFT JOIN nav_planet AS p ON (f.planetid=p.id)" + \
                        " WHERE f.ownerid="+ str(self.UserId)+" AND p.ownerid IS DISTINCT FROM "+ str(self.UserId) + \
                        " ORDER BY f.planetid" + \
                        " LIMIT 200"
                list_oRss = oConnExecuteAll(query)

                showGroup = False
                fleetgroup = []
                for list_oRs in list_oRss:
                    fleet = {}
                    fleet["index"] = index
                    fleet["fleet_name"] = list_oRs[0]
                    fleet["to_g"] = list_oRs[2]
                    fleet["to_s"] = list_oRs[3]
                    fleet["to_p"] = list_oRs[4]

                    if list_oRs[1] == oRs[10] and not hasAPlanetSelected: fleet["selected"] = True

                    fleetgroup.append(fleet)
                    index += 1
                    showGroup = True

                if showGroup: content.AssignValue("fleetgroup", fleetgroup)

                #
                # list merchant planets in the galaxy of the fleet
                #
                query = " SELECT id, galaxy, sector, planet" + \
                        " FROM nav_planet" + \
                        " WHERE ownerid=3"

                if oRs[12]:
                    query = query + " AND galaxy=" + str(oRs[12])

                query = query + " ORDER BY id"

                list_oRss = oConnExecuteAll(query)

                showGroup = False
                merchantplanetsgroup = []
                for list_oRs in list_oRss:
                    merchant = {}
                    merchant["index"] = index
                    merchant["to_g"] = list_oRs[1]
                    merchant["to_s"] = list_oRs[2]
                    merchant["to_p"] = list_oRs[3]

                    if list_oRs[0] == oRs[10] and not hasAPlanetSelected: merchant["selected"] = True

                    merchantplanetsgroup.append(merchant)
                    index += 1
                    showGroup = True

                if showGroup: content.AssignValue("merchantplanetsgroup", merchantplanetsgroup)

                content.Parse("move_fleet")

        # display action error
        if self.action_result != "": content.Parse(self.action_result)

        content.Parse("overview")

        if oRs[15]:
            planet_ownerid = oRs[15]
        else:
            planet_ownerid = self.UserId

        # display header
        if oRs[34] == 0 and oRs[17] == rSelf:
            self.CurrentPlanet = oRs[10]
            self.showHeader = True
        else:
            self.FillHeaderCredits(content)
            content.Parse("header_credits")
        
        #
        # display the list of ships in the fleet
        #
        query = "SELECT db_ships.id, fleets_ships.quantity," + \
                " signature, capacity, handling, speed, weapon_turrets, weapon_dmg_em+weapon_dmg_explosive+weapon_dmg_kinetic+weapon_dmg_thermal AS weapon_power, weapon_tracking_speed, hull, shield, recycler_output, long_distance_capacity, droppods," + \
                " buildingid, sp_can_build_on(" + str(oRs[10]) + ", db_ships.buildingid," + str(planet_ownerid) + ")=0 AS can_build" + \
                " FROM fleets_ships" + \
                "    LEFT JOIN db_ships ON (fleets_ships.shipid = db_ships.id)" + \
                " WHERE fleetid=" + str(fleetid) + \
                " ORDER BY db_ships.category, db_ships.label"
        oRss = oConnRows(query)

        shipCount = 0

        ships = []
        for oRs in oRss:
            ship = {}
            shipCount = shipCount + 1

            ship["id"] = oRs["id"]
            ship["quantity"] = oRs["quantity"]

            # assign ship label, description + characteristics
            ship["name"] = getShipLabel(oRs["id"])
            ship["description"] = getShipDescription(oRs["id"])

            ship["ship_signature"] = oRs["signature"]
            ship["ship_cargo"] = oRs["capacity"]
            ship["ship_handling"] = oRs["handling"]
            ship["ship_speed"] = oRs["speed"]

            ship["ship_turrets"] = oRs["weapon_turrets"]
            ship["ship_power"] = oRs["weapon_power"]
            ship["ship_tracking_speed"] = oRs["weapon_tracking_speed"]

            ship["ship_hull"] = oRs["hull"]
            ship["ship_shield"] = oRs["shield"]

            ship["ship_recycler_output"] = oRs["recycler_output"]
            ship["ship_long_distance_capacity"] = oRs["long_distance_capacity"]
            ship["ship_droppods"] = oRs["droppods"]

            if oRs["buildingid"]:
                if self.can_install_building and oRs["can_build"]:
                    ship["install"] = True
                else:
                    ship["cant_install"] = True

            ships.append(ship)
            
        content.AssignValue("shiplist", ships)

        content.Parse("display")

        return self.Display(content)

    def InstallBuilding(self, fleetid, shipid):
        
        oRs = oConnExecute("SELECT sp_start_ship_building_installation(" + str(self.fleet_owner_id) + "," + str(fleetid) + "," + str(shipid) + ")")

        if oRs == None: return

        if oRs[0] >= 0:
            # set as the new planet in == it has been colonized, the player expects to see its new planet after colonization
            self.CurrentPlanet = oRs[0]

            # invalidate planet list to reload it in == a planet has been colonized
            self.InvalidatePlanetList()
        elif oRs[0] == -7:
            self.action_result = "error_max_planets_reached"
        elif oRs[0] == -8:
            self.action_result = "error_deploy_enemy_ships"
        elif oRs[0] == -11:
            self.action_result = "error_deploy_too_many_safe_planets"

    def MoveFleet(self, fleetid):

        g = ToInt(self.request.POST.get("g"),-1)
        s = ToInt(self.request.POST.get("s"),-1)
        p = ToInt(self.request.POST.get("p"),-1)

        if g==-1 or s==-1 or p==-1:
            self.move_fleet_result = "bad_destination"
            return
        
        oRs = oConnExecute("SELECT sp_move_fleet(" + str(self.fleet_owner_id) + "," + str(fleetid) + "," + str(g) + "," + str(s) + "," + str(p) + ")")
        if oRs:
            res = oRs[0]

            if res == 0:
                if self.request.POST.get("movetype") == "1":
                    oConnDoQuery("UPDATE fleets SET next_waypointid = sp_create_route_unload_move(planetid) WHERE ownerid=" + str(self.fleet_owner_id) + " AND id=" + str(fleetid))
                elif self.request.POST.get("movetype") == "2":
                    oConnDoQuery("UPDATE fleets SET next_waypointid = sp_create_route_recycle_move(planetid) WHERE ownerid=" + str(self.fleet_owner_id) + " AND id=" + str(fleetid))

        else:
            res = 0
        
        if res == 0:
            self.move_fleet_result = "ok"
        elif res == -4: # new player or holidays protection
            self.move_fleet_result = "new_player_protection"
        elif res == -5: # long travel not possible
            self.move_fleet_result = "long_travel_impossible"
        elif res == -6: # not enough money
            self.move_fleet_result = "not_enough_credits"
        elif res == -7:
            self.move_fleet_result = "error_jump_from_require_empty_location"
        elif res == -8:
            self.move_fleet_result = "error_jump_protected_galaxy"
        elif res == -9:
            self.move_fleet_result = "error_jump_to_require_empty_location"
        elif res == -10:
            self.move_fleet_result = "error_jump_to_same_point_limit_reached"

    def Invade(self, fleetid, droppods, take):
        oRs = oConnExecute("SELECT sp_invade_planet(" + str(self.fleet_owner_id) + "," + str(fleetid) + ","+ str(droppods) +"," + str(ToBool(take, False)) +")")

        res = oRs[0]
        
        if res == -1:
            self.action_result = "error_soldiers"
        elif res == -2:
            self.action_result = "error_fleet"
        elif res == -3:
            self.action_result = "error_planet"
        elif res == -5:
            self.action_result = "error_invade_enemy_ships"

        if res > 0:
            self.InvalidatePlanetList()
            return HttpResponseRedirect("/s03/invasion/?id=" + str(res) + "+fleetid=" + str(fleetid))

    def ExecuteOrder(self, fleetid):

        if self.request.POST.get("action") == "invade":
            droppods = ToInt(self.request.POST.get("droppods"), 0)
            self.Invade(fleetid, droppods, self.request.POST.get("take") != "")
        elif self.request.POST.get("action") == "rename":
            fleetname = self.request.POST.get("newname").strip()
            if isValidObjectName(fleetname):
                oConnDoQuery("UPDATE fleets SET name="+dosql(fleetname)+" WHERE action=0 AND not engaged AND ownerid=" + str(self.UserId) + " AND id=" + str(fleetid))
            
        elif self.request.POST.get("action") == "assigncommander":
            # assign new commander
            if ToInt(self.request.POST.get("commander"), 0) != 0:
                commanderid = dosql(self.request.POST.get("commander"))
                oConnExecute("SELECT sp_commanders_assign(" + str(self.fleet_owner_id) + "," + str(commanderid) + ",NULL," + str(fleetid) + ")")
            else:
                # unassign current fleet commander
                oConnDoQuery("UPDATE fleets SET commanderid=null WHERE ownerid=" + str(self.fleet_owner_id) + " AND id=" + str(fleetid))

            oConnExecute("SELECT sp_update_fleet_bonus(" + str(fleetid) + ")")
        elif self.request.POST.get("action") == "move":
            self.MoveFleet(fleetid)

        if self.request.GET.get("action") == "share":
            oConnDoQuery("UPDATE fleets SET shared=not shared WHERE ownerid=" + str(self.fleet_owner_id) + " AND id=" + str(fleetid))
            return HttpResponseRedirect("/s03/fleet/?id=" + str(fleetid))
        elif self.request.GET.get("action") == "abandon":
            oConnExecute("SELECT sp_abandon_fleet(" + str(self.UserId) + "," + str(fleetid) + ")")
        elif self.request.GET.get("action") == "attack":
            oConnDoQuery("UPDATE fleets SET attackonsight=firepower > 0 WHERE ownerid=" + str(self.fleet_owner_id) + " AND id=" + str(fleetid))
        elif self.request.GET.get("action") == "defend":
            oConnDoQuery("UPDATE fleets SET attackonsight=False WHERE ownerid=" + str(self.fleet_owner_id) + " AND id=" + str(fleetid))
        elif self.request.GET.get("action") == "recycle":
            oRs = oConnExecute("SELECT sp_start_recycling(" + str(self.fleet_owner_id) + "," + str(fleetid) + ")")
            if oRs[0] == -2:
                self.action_result = "error_recycling"
            
        elif self.request.GET.get("action") == "stoprecycling":
            oConnExecute("SELECT sp_cancel_recycling(" + str(self.fleet_owner_id) + "," + str(fleetid) + ")")
        elif self.request.GET.get("action") == "stopwaiting":
            oConnExecute("SELECT sp_cancel_waiting(" + str(self.fleet_owner_id) + "," + str(fleetid) + ")")
        elif self.request.GET.get("action") == "merge":
            destfleetid = ToInt(self.request.GET.get("with"), 0)
            oConnExecute("SELECT sp_merge_fleets(" + str(self.UserId) + "," + str(fleetid) + ","+ str(destfleetid) +")")
        elif self.request.GET.get("action") == "return":
            oConnExecute("SELECT sp_cancel_move(" + str(self.fleet_owner_id) + "," + str(fleetid) + ")")
        elif self.request.GET.get("action") == "install":
            shipid = ToInt(self.request.GET.get("s"), 0)
            self.InstallBuilding(fleetid, shipid)
        elif self.request.GET.get("action") == "warp":
            oConnExecute("SELECT sp_warp_fleet(" + str(self.fleet_owner_id) + "," + str(fleetid) + ")")
