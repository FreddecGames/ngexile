# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.max_ore = 2.0
        self.max_hydrocarbon = 2.0
        self.max_energy = 2.0
        self.max_workers = 2.0

        self.max_speed = 1.3
        self.max_shield = 1.4
        self.max_handling = 1.75
        self.max_targeting = 1.75
        self.max_damages = 1.3
        self.max_signature = 1.2

        self.max_recycling = 1.1

        self.max_build = 3
        self.max_ship = 3

        self.selectedMenu = "commanders"

        CommanderId = ToInt(request.GET.get("id"), 0)
        NewName = request.GET.get("name")

        if request.GET.get("a") == "rename":
            return self.RenameCommander(CommanderId, NewName)
        elif request.GET.get("a") == "edit":
            return self.EditCommander(CommanderId)
        elif request.GET.get("a") == "fire":
            return self.FireCommander(CommanderId)
        elif request.GET.get("a") == "engage":
            return self.EngageCommander(CommanderId)
        elif request.GET.get("a") == "skills":
            return self.DisplayCommanderEdition(CommanderId)
        elif request.GET.get("a") == "train":
            return self.TrainCommander(CommanderId)
        else:
            return self.ListCommanders()

    def DisplayBonus(self, item, bonus, value):
        if value > 0:
            bonus["bonus"] = "+" + str(value)
            bonus["positive"] = True
        elif value < 0:
            bonus["bonus"] = value
            bonus["negative"] = True
        else:
            bonus["bonus"] = value

        item["bonuses"].append(bonus)

    # List the commanders owned by the player
    def ListCommanders(self):
        content = getTemplate(self.request, "s03/commanders")

        content.setValue("planetid", self.CurrentPlanet)

        # generate new commanders if needed for the player
        oConnExecute("SELECT sp_commanders_check_new_commanders(" + str(self.userId) + ")")

        # retrieve how many commanders are controled by the player
        oRs = oConnExecute("SELECT int4(count(1)) FROM commanders WHERE recruited <= now() AND ownerid=" + str(self.userId))
        can_engage_commander = oRs[0] < self.oPlayerInfo["mod_commanders"]

        # Retrieve all the commanders belonging to the player
        query = "SELECT c.id, c.name, c.recruited, points, added, salary, can_be_fired, " + \
                " p.id, p.galaxy, p.sector, p.planet, p.name, " + \
                " f.id, f.name, " + \
                " c.mod_production_ore, c.mod_production_hydrocarbon, c.mod_production_energy, " + \
                " c.mod_production_workers, c.mod_fleet_speed, c.mod_fleet_shield, " + \
                " c.mod_fleet_handling, c.mod_fleet_tracking_speed, c.mod_fleet_damage, c.mod_fleet_signature, "  + \
                " c.mod_construction_speed_buildings, c.mod_construction_speed_ships, last_training < now()-interval '1 day', sp_commanders_prestige_to_train(c.ownerid, c.id), salary_increases < 20" + \
                " FROM commanders AS c" + \
                "    LEFT JOIN fleets AS f ON (c.id=f.commanderid)" + \
                "    LEFT JOIN nav_planet AS p ON (c.id=p.commanderid)" + \
                " WHERE c.ownerid=" + str(self.userId) + \
                " ORDER BY upper(c.name)"
        oRss = oConnExecuteAll(query)

        available_commanders_count = 0
        commanders_count = 0

        commanders = []
        content.setValue("commander_list", commanders)
        available_commanders = []
        content.setValue("available_commanders", available_commanders)
        for oRs in oRss:
            item = {}
            
            item["id"] = oRs[0]
            item["name"] = oRs[1]
            item["recruited"] = oRs[2]
            item["added"] = oRs[4]
            item["salary"] = oRs[5]

            if oRs[2] == None:
                available_commanders.append(item)
                section = "available_commanders"
                available_commanders_count = available_commanders_count + 1

                if can_engage_commander:
                    item["can_engage"] = True
                else:
                    item["cant_engage"] = True

            else:
                commanders.append(item)
                section = "commanders"
                commanders_count = commanders_count + 1

                if oRs[6]:
                    item["can_fire"] = True
                else:
                    item["cant_fire"] = True

            if oRs[7] == None: # commander is not assigned to a planet
                if oRs[12] == None: # nor to a fleet
                    item["not_assigned"] = True
                else:
                    item["fleetid"] = oRs[12]
                    item["commandment"] = oRs[13]
                    item["fleet_command"] = True

            else:
                item["planetid"] = oRs[7]
                item["g"] = oRs[8]
                item["s"] = oRs[9]
                item["p"] = oRs[10]
                item["commandment"] = oRs[11]
                item["planet_command"] = True

            #
            # browse the possible bonus
            #
            item["bonuses"] = []
            for i in range(14, 26):
                if oRs[i] != 1.0:
                    bonus = {}
                    bonus["description" + str(i)] = True
                    self.DisplayBonus(item, bonus, round((oRs[i]-1.0)*100))

            if oRs[26] and oRs[28]:
                item["prestige"] = oRs[27]
                item["train"] = True
            else:
                if oRs[28]:
                    item["cant_train"] = True
                else:
                    item["cant_train_anymore"] = True

            if oRs[3] > 0:
                item["points"] = oRs[3]
                item["levelup"] = True

        content.setValue("max_commanders", int(self.oPlayerInfo["mod_commanders"]))

        if available_commanders_count == 0: content.Parse("available_commanders_nocommander")
        if commanders_count == 0: content.Parse("commanders_nocommander")

        return self.display(content)

    def DisplayCommanderEdition(self, CommanderId):

        content = getTemplate(self.request, "s03/commanders")

        content.setValue("commanderid", CommanderId)

        if CommanderId != 0:

            query = "SELECT mod_production_ore, mod_production_hydrocarbon, mod_production_energy," + \
                    " mod_production_workers, mod_fleet_speed, mod_fleet_shield, mod_fleet_handling," + \
                    " mod_fleet_tracking_speed, mod_fleet_damage, mod_fleet_signature," + \
                    " mod_construction_speed_buildings, mod_construction_speed_ships," + \
                    " points, name" + \
                    " FROM commanders WHERE points > 0 AND id=" + str(CommanderId) + " AND ownerid=" + str(self.userId)
            oRs = oConnExecute(query)

            if oRs == None:
                # commander not found !
               return HttpResponseRedirect("/s03/commanders/")

            content.setValue("name", oRs[13])
            content.setValue("maxpoints", oRs[12])

            content.setValue("ore", str(oRs[0]).replace(",", "."))
            content.setValue("hydrocarbon", str(oRs[1]).replace(",", "."))
            content.setValue("energy", str(oRs[2]).replace(",", "."))
            content.setValue("workers", str(oRs[3]).replace(",", "."))

            content.setValue("speed", str(oRs[4]).replace(",", "."))
            content.setValue("shield", str(oRs[5]).replace(",", "."))
            content.setValue("handling", str(oRs[6]).replace(",", "."))
            content.setValue("targeting", str(oRs[7]).replace(",", "."))
            content.setValue("damages", str(oRs[8]).replace(",", "."))
            content.setValue("signature", str(oRs[9]).replace(",", "."))

            content.setValue("build", str(oRs[10]).replace(",", "."))
            content.setValue("ship", str(oRs[11]).replace(",", "."))

            content.setValue("max_ore", str(self.max_ore).replace(",", "."))
            content.setValue("max_hydrocarbon", str(self.max_hydrocarbon).replace(",", "."))
            content.setValue("max_energy", str(self.max_energy).replace(",", "."))
            content.setValue("max_workers", str(self.max_workers).replace(",", "."))

            content.setValue("max_speed", str(self.max_speed).replace(",", "."))
            content.setValue("max_shield", str(self.max_shield).replace(",", "."))
            content.setValue("max_handling", str(self.max_handling).replace(",", "."))
            content.setValue("max_targeting", str(self.max_targeting).replace(",", "."))
            content.setValue("max_damages", str(self.max_damages).replace(",", "."))
            content.setValue("max_signature", str(self.max_signature).replace(",", "."))

            content.setValue("max_build", str(self.max_build).replace(",", "."))
            content.setValue("max_ship", str(self.max_ship).replace(",", "."))

            content.setValue("max_recycling", str(self.max_recycling).replace(",", "."))

        content.Parse("editcommander")

        return self.display(content)

    def Max(self, a,b):
        if a<b:
            Max=b
        else:
            Max=a

    def EditCommander(self, CommanderId):

        ore = max(0, ToInt(self.request.POST.get("ore"), 0))
        hydrocarbon = max(0, ToInt(self.request.POST.get("hydrocarbon"), 0))
        energy = max(0, ToInt(self.request.POST.get("energy"), 0))
        workers = max(0, ToInt(self.request.POST.get("workers"), 0))

        fleetspeed = max(0, ToInt(self.request.POST.get("fleet_speed"), 0))
        fleetshield = max(0, ToInt(self.request.POST.get("fleet_shield"), 0))
        fleethandling = max(0, ToInt(self.request.POST.get("fleet_handling"), 0))
        fleettargeting = max(0, ToInt(self.request.POST.get("fleet_targeting"), 0))
        fleetdamages = max(0, ToInt(self.request.POST.get("fleet_damages"), 0))
        fleetsignature = max(0, ToInt(self.request.POST.get("fleet_signature"), 0))

        build = max(0, ToInt(self.request.POST.get("buildindspeed"), 0))
        ship = max(0, ToInt(self.request.POST.get("shipconstructionspeed"), 0))

        total = ore + hydrocarbon + energy + workers + fleetspeed + fleetshield + fleethandling + fleettargeting + fleetdamages + fleetsignature + build + ship

        query = "UPDATE commanders SET" + \
                "    mod_production_ore=mod_production_ore + 0.01*" + str(ore) + \
                "    ,mod_production_hydrocarbon=mod_production_hydrocarbon + 0.01*" + str(hydrocarbon) + \
                "    ,mod_production_energy=mod_production_energy + 0.1*" + str(energy) + \
                "    ,mod_production_workers=mod_production_workers + 0.1*" + str(workers) + \
                "    ,mod_fleet_speed=mod_fleet_speed + 0.02*" + str(fleetspeed) + \
                "    ,mod_fleet_shield=mod_fleet_shield + 0.02*" + str(fleetshield) + \
                "    ,mod_fleet_handling=mod_fleet_handling + 0.05*" + str(fleethandling) + \
                "    ,mod_fleet_tracking_speed=mod_fleet_tracking_speed + 0.05*" + str(fleettargeting) + \
                "    ,mod_fleet_damage=mod_fleet_damage + 0.02*" + str(fleetdamages) + \
                "    ,mod_fleet_signature=mod_fleet_signature + 0.02*" + str(fleetsignature) + \
                "    ,mod_construction_speed_buildings=mod_construction_speed_buildings + 0.05*" + str(build) + \
                "    ,mod_construction_speed_ships=mod_construction_speed_ships + 0.05*" + str(ship) + \
                "    ,points=points-" + str(total) + \
                " WHERE ownerid=" + str(self.userId) + " AND id=" + str(CommanderId) + " AND points >= " + str(total)

        oConnDoQuery(query)

        query = "SELECT sp_commanders_update_salary(" + str(self.userId) + ", " + str(CommanderId) + ")"
        oConnDoQuery(query)

        query = "SELECT mod_production_ore, mod_production_hydrocarbon, mod_production_energy," + \
                    " mod_production_workers, mod_fleet_speed, mod_fleet_shield, mod_fleet_handling," + \
                    " mod_fleet_tracking_speed, mod_fleet_damage, mod_fleet_signature," + \
                    " mod_construction_speed_buildings, mod_construction_speed_ships" + \
                    " FROM commanders" + \
                    " WHERE id=" + str(CommanderId) + " AND ownerid=" + str(self.userId)
        oRs = oConnExecute(query)

        if oRs[0] <= self.max_ore+0.0001 and oRs[1] <= self.max_hydrocarbon+0.0001 and oRs[2] <= self.max_energy+0.0001 and oRs[3] <= self.max_workers+0.0001 and \
            oRs[4] <= self.max_speed+0.0001 and oRs[5] <= self.max_shield+0.0001 and oRs[6] <= self.max_handling+0.0001 and oRs[7] <= self.max_targeting+0.0001 and oRs[8] <= self.max_damages+0.0001 and oRs[9] <= self.max_signature+0.0001 and \
            oRs[10] <= self.max_build+0.0001 and oRs[11] <= self.max_ship+0.0001:

            query = "SELECT sp_update_fleet_bonus(id) FROM fleets WHERE commanderid=" + str(CommanderId)
            oConnDoQuery(query)

            query = "SELECT sp_update_planet(id) FROM nav_planet WHERE commanderid=" + str(CommanderId)
            oConnDoQuery(query)

        return HttpResponseRedirect("/s03/commanders/")

    def RenameCommander(self, CommanderId, NewName):

        query = "SELECT sp_commanders_rename(" + str(self.userId) + "," + str(CommanderId) + "," + dosql(NewName) + ")"
        oConnDoQuery(query)
        return HttpResponseRedirect("/s03/commanders/")

    def EngageCommander(self, CommanderId):

        query = "SELECT sp_commanders_engage(" + str(self.userId) + "," + str(CommanderId) + ")"
        oConnDoQuery(query)
        return HttpResponseRedirect("/s03/commanders/")

    def FireCommander(self, CommanderId):

        query = "SELECT sp_commanders_fire(" + str(self.userId) + "," + str(CommanderId) + ")"
        oConnDoQuery(query)
        return HttpResponseRedirect("/s03/commanders/")

    def TrainCommander(self, CommanderId):

        query = "SELECT sp_commanders_train(" + str(self.userId) + "," + str(CommanderId) + ")"
        oConnDoQuery(query)
        return HttpResponseRedirect("/s03/commanders/")
