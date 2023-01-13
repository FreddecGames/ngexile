from .base import *


class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        self.selectedMenu = "orbit"

        self.showHeader = True

        self.e_no_error = 0
        self.e_bad_name = 1
        self.e_already_exists = 2

        self.fleet_creation_error = ""

        if request.GET.get("a", "") == "new":
            self.NewFleet()

        return self.DisplayFleets()

    def DisplayFleets(self):
        
        content = GetTemplate(self.request, "planet-orbit")

        content.AssignValue("planetid", str(self.CurrentPlanet))

        # list the fleets near the planet
        query = "SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername," + \
                " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation," + \
                " destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_ownerid, destplanet_owner_name, destplanet_owner_relation," + \
                " action, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers, ownerid, owner_name" + \
                " FROM vw_fleets " + \
                " WHERE planetid="+ str(self.CurrentPlanet) +" AND action != 1 AND action != -1" + \
                " ORDER BY upper(name)"
        oRss = oConnExecuteAll(query)

        if not oRss:
            content.Parse("nofleets")
        else:
            fleets = []
            content.AssignValue("fleets", fleets)
            
            for oRs in oRss:
                manage = False
                trade = False
                
                fleet = {}

                fleet["id"] = oRs[0]
                fleet["name"] = oRs[1]
                fleet["size"] = oRs[4]
                fleet["signature"] = oRs[5]

                fleet["ownerid"] = oRs[32]
                fleet["ownername"] = oRs[33]

                fleet["cargo"] = oRs[27]+oRs[28]+oRs[29]+oRs[30]+oRs[31]
                fleet["cargo_ore"] = oRs[27]
                fleet["cargo_hydrocarbon"] = oRs[28]
                fleet["cargo_scientists"] = oRs[29]
                fleet["cargo_soldiers"] = oRs[30]
                fleet["cargo_workers"] = oRs[31]

                if oRs[8]:
                    fleet["commanderid"] = oRs[8]
                    fleet["commandername"] = oRs[9]
                    fleet["commander"] = True
                else:
                    fleet["nocommander"] = True

                if oRs[26] == 2:
                    fleet["recycling"] = True
                elif oRs[3]:
                    fleet["fighting"] = True
                else:
                    fleet["patrolling"] = True

                if oRs[17] == rHostile or oRs[17] == rWar:
                    fleet["enemy"] = True
                elif oRs[17] == rAlliance:
                    fleet["ally"] = True
                elif oRs[17] == rFriend:
                    fleet["friend"] = True
                elif oRs[17] == rSelf:
                    fleet["owner"] = True

                if manage:
                    fleet["manage"] = True
                else:
                    fleet["cant_manage"] = True

                if trade:
                    fleet["trade"] = True
                else:
                    fleet["cant_trade"] = True
                
                fleets.append(fleet)

        # list the ships on the planet to create a new fleet
        query = "SELECT shipid, quantity," + \
                " signature, capacity, handling, speed, (weapon_dmg_em + weapon_dmg_explosive + weapon_dmg_kinetic + weapon_dmg_thermal) AS weapon_power, weapon_turrets, weapon_tracking_speed, hull, shield, recycler_output, long_distance_capacity, droppods" + \
                " FROM planet_ships LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id)" + \
                " WHERE planetid=" + str(self.CurrentPlanet) + \
                " ORDER BY category, label"

        oRss = oConnRows(query)
        if not oRss:
            content.Parse("noships")
        else:
            ships = []
            content.AssignValue("ships", ships)
            
            for oRs in oRss:
                ship = {}
                
                ship["id"] = oRs["shipid"]
                ship["quantity"] = oRs["quantity"]

                ship["name"] = getShipLabel(oRs["shipid"])

                if self.fleet_creation_error != "": ship["ship_quantity"] = ToInt(self.request.POST.get("s" + str(oRs["shipid"]), 0), 0)

                # assign ship description
                ship["description"] = getShipDescription(oRs["shipid"])

                ship["ship_signature"] = oRs["signature"]
                ship["ship_cargo"] = oRs["capacity"]
                ship["ship_handling"] = oRs["handling"]
                ship["ship_speed"] = oRs["speed"]

                if oRs["weapon_power"] > 0:
                    ship["ship_turrets"] = oRs["weapon_turrets"]
                    ship["ship_power"] = oRs["weapon_power"]
                    ship["ship_tracking_speed"] = oRs["weapon_tracking_speed"]
                    ship["attack"] = True

                ship["ship_hull"] = oRs["hull"]

                if oRs["shield"] > 0:
                    ship["ship_shield"] = oRs["shield"]
                    ship["shield"] = True

                if oRs["recycler_output"] > 0:
                    ship["ship_recycler_output"] = oRs["recycler_output"]
                    ship["recycler_output"] = True

                if oRs["long_distance_capacity"] > 0:
                    ship["ship_long_distance_capacity"] = oRs["long_distance_capacity"]
                    ship["long_distance_capacity"] = True

                if oRs["droppods"] > 0:
                    ship["ship_droppods"] = oRs["droppods"]
                    ship["droppods"] = True
                
                ships.append(ship)

            content.Parse("new")

        # Assign the fleet name passed in form body
        if self.fleet_creation_error != "":
            content.AssignValue("fleetname", self.request.POST.get("name"))

            content.Parse(self.fleet_creation_error)
            content.Parse("error")

        return self.Display(content)

    #
    # Create the new fleet
    #
    def NewFleet(self):
        fleetname = self.request.POST.get("name", "").strip()

        if not isValidObjectName(fleetname):
            self.fleet_creation_error = "fleet_name_invalid"
            return

        # retrieve all ships id that exists in shipsArray
        oRss = oConnExecuteAll("SELECT id FROM db_ships")

        shipsArray = oRss
        shipsCount = len(oRss)

        # create a new fleet at the current planet with the given name
        
        oRs = oConnExecute("SELECT sp_create_fleet(" + str(self.UserId) + "," + str(self.CurrentPlanet) + "," + dosql(fleetname) + ")")
        if not oRs:
            return
        
        fleetid = oRs[0]

        if fleetid < 0:
            if fleetid == -3:
                self.fleet_creation_error = "fleet_too_many"
            else:
                self.fleet_creation_error = "fleet_name_already_used"
            
            return
        
        cant_use_ship = False

        for i in shipsArray:
            shipid = i[0]
            quantity = ToInt(self.request.POST.get("s" + str(shipid)), 0)

            # add the ships type by type
            if quantity > 0:
                oRs = oConnExecute("SELECT * FROM sp_transfer_ships_to_fleet(" + str(self.UserId) + ", " + str(fleetid) + ", " + str(shipid) + ", " + str(quantity) + ")")
                cant_use_ship = cant_use_ship or oRs[0] == 3

        # delete the fleet if there is no ships in it
        oConnDoQuery("DELETE FROM fleets WHERE size=0 AND id=" + str(fleetid) + " AND ownerid=" + str(self.UserId))

        if cant_use_ship and self.fleet_creation_error == "": self.fleet_creation_error = "ship_cant_be_used"
