from .base import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        self.selectedMenu = "ships"

        self.showHeader = True

        Action = request.GET.get("a", "").lower()

        # retrieve which page to display
        self.ShipFilter = ToInt(request.GET.get("f", -1), -1)

        if self.ShipFilter == -1:
            self.ShipFilter = ToInt(request.session.get("shipyardfilter", 0), 0)

        if self.ShipFilter < 0 or self.ShipFilter > 3: self.ShipFilter = 0

        request.session["shipyardfilter"] = self.ShipFilter

        if Action == "build" or Action == "bui1d":
            return self.BuildShips()

        if Action == "recycle": return self.RecycleShips()

        if Action == "cancel":
            QueueId = ToInt(request.GET.get("q"),0)

            if QueueId != 0: return self.CancelQueue(QueueId)

        self.RetrieveData()

        if request.GET.get("recycle", "") != "":
            return self.ListRecycleShips()
        else:
            return self.ListShips()

    # retrieve planet and player information
    def RetrieveData(self):
        
        # Retrieve recordset of current planet
        query = "SELECT ore_capacity, hydrocarbon_capacity, energy_capacity, workers_capacity"+ \
                " FROM vw_planets WHERE id="+str(self.CurrentPlanet)
        self.oPlanet = oConnExecute(query)

    def displayQueue(self, content, planetid):
        # list queued ships and ships under construction

        query = "SELECT id, shipid, remaining_time, quantity, end_time, recycle, required_shipid, int4(cost_ore*const_recycle_ore(ownerid)), int4(cost_hydrocarbon*const_recycle_hydrocarbon(ownerid)), cost_ore, cost_hydrocarbon, cost_energy, crew" + \
                " FROM vw_ships_under_construction" + \
                " WHERE planetid=" + str(planetid) + \
                " ORDER BY start_time, shipid"

        oRss = oConnExecuteAll(query)

        buildingcount = 0
        queuecount = 0
        
        queues = []
        underconstructions = []

        if oRss:
            for oRs in oRss:
                item = {}
            
                item["queueid"] = oRs[0]
                item["id"] = oRs[1]
                item["name"] = getShipLabel(oRs[1])
    
                if int(oRs[2]) > 0:
                    item["remainingtime"] = oRs[2]
                else:
                    item["remainingtime"] = 0
    
                item["quantity"] = oRs[3]
    
                if oRs[5]:
                    item["ore"] = oRs[3]*oRs[7]
                    item["hydrocarbon"] = oRs[3]*oRs[8]
                    item["energy"] = 0
                    item["crew"] = 0
                else:
                    item["ore"] = oRs[3]*oRs[9]
                    item["hydrocarbon"] = oRs[3]*oRs[10]
                    item["energy"] = oRs[3]*oRs[11]
                    item["crew"] = oRs[3]*oRs[12]
    
                if oRs[6]: item["required_ship_name"] = getShipLabel(oRs[6])
    
                if oRs[4]:
                    if oRs[5]:
                        item["recycle"] = True
                    else:
                        item["cancel"] = True
    
                    if oRs[6]: item["required_ship"] = True
    
                    item["ship"] = True
                    underconstructions.append(item)
                else:
                    if oRs[5]: item["recycle"] = True
                    if oRs[6]: item["required_ship"] = True
    
                    item["cancel"] = True
                    item["ship"] = True
                    queues.append(item)
                
        content.AssignValue("queues", queues)
        content.AssignValue("underconstructions", underconstructions)

    # List all the available ships for construction
    def ListShips(self):

        # list ships that can be built on the planet
        query = "SELECT id, category, name, cost_ore, cost_hydrocarbon, cost_energy, workers, crew, capacity," + \
                " construction_time, hull, shield, weapon_power, weapon_ammo, weapon_tracking_speed, weapon_turrets, signature, speed," + \
                " handling, buildingid, recycler_output, droppods, long_distance_capacity, quantity, buildings_requirements_met, research_requirements_met," + \
                " required_shipid, required_ship_count, COALESCE(new_shipid, id) AS shipid, cost_prestige, upkeep, required_vortex_strength, mod_leadership" + \
                " FROM vw_ships WHERE planetid=" + str(self.CurrentPlanet)

        if self.ShipFilter == 1:
            self.selectedMenu = "shipyard_military"
            query = query + " AND weapon_power > 0 AND required_shipid IS NULL" # military ships only
        elif self.ShipFilter == 2:
            self.selectedMenu = "shipyard_unarmed"
            query = query + " AND weapon_power = 0 AND required_shipid IS NULL" # non-military ships
        elif self.ShipFilter == 3:
            self.selectedMenu = "shipyard_upgrade"
            query = query + " AND required_shipid IS NOT NULL" # upgrade ships only
        query = query + " ORDER BY category, id"
        
        oRss = oConnRows(query)

        content = GetTemplate(self.request, "planet-ships")

        content.AssignValue("planetid", self.CurrentPlanet)
        content.AssignValue("filter", self.ShipFilter)

        # number of items in category
        itemCount = 0

        # number of ships types that can be built
        buildable = 0

        lastCategory = -1 

        categories = []

        count = 0
        for oRs in oRss:
            if (oRs["quantity"] > 0) or oRs["research_requirements_met"]:
                CatId = oRs["category"]

                if CatId != lastCategory:
                    category = {'id':CatId, 'ships':[]}
                    categories.append(category)
                    
                    lastCategory = CatId

                ship = {}
                category['ships'].append(ship)
                count += 1

                ShipId = oRs["shipid"]

                ship["id"] = oRs["id"]
                ship["name"] = getShipLabel(ShipId)

                if oRs["required_shipid"]:
                    ship["required_ship_name"] = getShipLabel(oRs["required_shipid"])
                    ship["required_ship_available"] = oRs["required_ship_count"]
                    if oRs["required_ship_count"] == 0: ship["required_ship_none_available"] = True
                    ship["required_ship"] = True

                if oRs["cost_prestige"] > 0:
                    ship["required_pp"] = oRs["cost_prestige"]
                    ship["pp"] = self.oPlayerInfo["prestige_points"]
                    if oRs["cost_prestige"] > self.oPlayerInfo["prestige_points"]: ship["required_pp_not_enough"] = True

                ship["ore"] = oRs["cost_ore"]
                ship["hydrocarbon"] = oRs["cost_hydrocarbon"]
                ship["energy"] = oRs["cost_energy"]
                ship["workers"] = oRs["workers"]
                ship["crew"] = oRs["crew"]
                ship["upkeep"] = oRs["upkeep"]

                ship["quantity"] = oRs["quantity"]

                ship["time"] = oRs["construction_time"]

                # assign ship description
                ship["description"] = getShipDescription(oRs["shipid"])

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
                ship["ship_required_vortex_strength"] = oRs["required_vortex_strength"]

                ship["ship_leadership"] = oRs["mod_leadership"]

                if oRs["research_requirements_met"]:
                    ship["construction_time"] = True

                    notenoughresources = False

                    if oRs["cost_ore"] > self.oPlanet[0]:
                        ship["not_enough_ore"] = True
                        notenoughresources = True
                    
                    if oRs["cost_hydrocarbon"] > self.oPlanet[1]:
                        ship["not_enough_hydrocarbon"] = True
                        notenoughresources = True
                    
                    if oRs["cost_energy"] > self.oPlanet[2]:
                        ship["not_enough_energy"] = True
                        notenoughresources = True
                    
                    if oRs["crew"] > self.oPlanet[3]:
                        ship["not_enough_crew"] = True
                        notenoughresources = True

                    can_build = True

                    if not oRs["buildings_requirements_met"]:
                        ship["buildings_required"] = True
                        can_build = False

                    if notenoughresources:
                        ship["notenoughresources"] = True
                        can_build = False

                    if can_build:
                        ship["build"] = True
                        buildable = buildable + 1
                    
                else:
                    ship["no_construction_time"] = True
                    ship["cant_build"] = True

                for i in retrieveShipsReqCache():
                    if i[0] == ShipId:
                        ship["building"] = getBuildingLabel(i[1])
                        ship["buildingsrequired"] = True
        
        if count == 0: content.Parse("no_shipyard")
        else: content.AssignValue("categories", categories)
        
        if buildable > 0: content.Parse("build")
        else: content.Parse("nobuild")

        self.displayQueue(content, str(self.CurrentPlanet))

        return self.Display(content)

    # List all the available ships for recycling
    def ListRecycleShips(self):

        self.selectedMenu = "shipyard_recycle"

        # list ships that are on the planet
        query = "SELECT id, category, name, int4(cost_ore * const_recycle_ore(planet_ownerid)) AS cost_ore, int4(cost_hydrocarbon * const_recycle_hydrocarbon(planet_ownerid)) AS cost_hydrocarbon, cost_credits, workers, crew, capacity," + \
                " int4(const_ship_recycling_multiplier() * construction_time) as construction_time, hull, shield, weapon_power, weapon_ammo, weapon_tracking_speed, weapon_turrets, signature, speed," + \
                " handling, buildingid, recycler_output, droppods, long_distance_capacity, quantity, true, true," + \
                " NULL, 0, COALESCE(new_shipid, id) AS shipid" + \
                " FROM vw_ships" + \
                " WHERE quantity > 0 AND planetid=" + str(self.CurrentPlanet)

        oRss = oConnRows(query)
        
        content = GetTemplate(self.request, "shipyard-recycle")

        content.AssignValue("planetid", str(self.CurrentPlanet))
        content.AssignValue("filter", self.ShipFilter)

        # number of items in category
        itemCount = 0

        # number of ships types that can be built
        buildable = 0

        lastCategory = -1 

        categories = []

        count = 0
        for oRs in oRss:
            CatId = oRs["category"]

            if CatId != lastCategory:
                category = {'id':CatId, 'ships':[]}
                categories.append(category)
                
                lastCategory = lastCategory

            ship = {}
            category['ships'].append(ship)

            itemCount = itemCount + 1

            ship["id"] = oRs["id"]
            ship["name"] = getShipLabel(oRs["shipid"])

            ship["ore"] = oRs["cost_ore"]
            ship["hydrocarbon"] = oRs["cost_hydrocarbon"]
            ship["credits"] = oRs["cost_credits"]
            ship["workers"] = oRs["workers"]
            ship["crew"] = oRs["crew"]

            ship["quantity"] = oRs["quantity"]

            ship["time"] = oRs["construction_time"]

            # assign ship description
            ship["description"] = getShipDescription(oRs["shipid"])

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

            ship["construction_time"] = True

            can_build = True

            ship["build"] = True
            buildable = buildable + 1

            count = count + 1

        if count == 0: content.Parse("no_shipyard")
        content.AssignValue("categories", categories)
        
        if buildable > 0: content.Parse("build")
        else: content.Parse("nobuild")

        self.displayQueue(content, str(self.CurrentPlanet))

        return self.Display(content)

    # build ships

    def StartShip(self, ShipId, quantity):
        connExecuteRetryNoRecords("SELECT sp_start_ship(" + str(self.CurrentPlanet) + "," + str(ShipId) + "," + str(quantity) + ", false)")

    def BuildShips(self):

        for i in retrieveShipsCache():
            shipid = i[0]

            quantity = ToInt(self.request.POST.get("s" + str(shipid)), 0)
            if quantity > 0: self.StartShip(shipid, quantity)
            
        return HttpResponseRedirect("/s03/planet-ships/?f="+str(self.ShipFilter))
        
    # recycle ships

    def RecycleShip(self, ShipId, quantity):
        connExecuteRetryNoRecords("SELECT sp_start_ship_recycling(" + str(self.CurrentPlanet) + "," + str(ShipId) + "," + str(quantity) + ")")

    def RecycleShips(self):

        for i in retrieveShipsCache():
            shipid = i[0]

            quantity = ToInt(self.request.POST.get("s" + str(shipid)), 0)
            if quantity > 0: self.RecycleShip(shipid, quantity)
            
        return HttpResponseRedirect("/s03/planet-ships/?recycle=1")

    def CancelQueue(self, QueueId):
        connExecuteRetryNoRecords("SELECT sp_cancel_ship(" + str(self.CurrentPlanet) + ", " + str(QueueId) + ")")
        
        if self.request.GET.get("recycle", "") != "":
            return HttpResponseRedirect("/s03/planet-ships/?recycle=1")
        else:
            return HttpResponseRedirect("/s03/planet-ships/?f="+str(self.ShipFilter))
