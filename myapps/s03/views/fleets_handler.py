# -*- coding: utf-8 -*-

import re

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from myapps.s03.lib.exile import *
from myapps.s03.lib.template import *

from myapps.s03.views.cache import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        if maintenance and not request.user.is_superuser : return HttpResponseRedirect("/")

        self.UserId = ToInt(request.session.get(sUser), 0)
        if self.UserId == 0: return HttpResponseRedirect("/")

        action = request.GET.get("a")

        # change category of a fleet
        if action == "setcat":
            fleetid = ToInt(request.GET.get("id"), 0)
            oldCat = ToInt(request.GET.get("old"), 0)
            newCat = ToInt(request.GET.get("new"), 0)

            oRs = oConnExecute("SELECT sp_fleets_set_category(" + str(self.UserId) + "," + str(fleetid) + "," + str(oldCat) + "," + str(newCat) + ")")
            if oRs and oRs[0]:
                content = GetTemplate(self.request, "s03/fleets-handler")

                content.AssignValue("id", fleetid)
                content.AssignValue("old", oldCat)
                content.AssignValue("new", newCat)
                content.Parse("fleet_category_changed")

                return render(self.request, content.template, content.data)

        # create a new category
        if action == "newcat":
            name = request.GET.get("name")

            content = GetTemplate(self.request, "s03/fleets-handler")

            if self.isValidCategoryName(name):
                oRs = oConnExecute("SELECT sp_fleets_categories_add(" + str(self.UserId) + "," + dosql(name) + ")")

                if oRs:
                    content.AssignValue("id", oRs[0])
                    content.AssignValue("label", name)
                    content.Parse("category")

                    return render(self.request, content.template, content.data)

            else:
                content.Parse("category_name_invalid")

                return render(self.request, content.template, content.data)

        # rename a category
        if action == "rencat":
            name = request.GET.get("name")
            catid = ToInt(request.GET.get("id"), 0)

            content = GetTemplate(self.request, "s03/fleets-handler")

            if name == "":
                oRs = oConnExecute("SELECT sp_fleets_categories_delete(" + str(self.UserId) + "," + str(catid) + ")")
                if oRs:
                    content.AssignValue("id", catid)
                    content.AssignValue("label", name)
                    content.Parse("category")

                    return render(self.request, content.template, content.data)

            elif self.isValidCategoryName(name):
                oRs = oConnExecute("SELECT sp_fleets_categories_rename(" + str(self.UserId) + "," + str(catid) + "," + dosql(name) + ")")

                if oRs:
                    content.AssignValue("id", catid)
                    content.AssignValue("label", name)
                    content.Parse("category")

                    return render(self.request, content.template, content.data)

            else:
                content.Parse("category_name_invalid")

                return render(self.request, content.template, content.data)

        # retrieve list of fleets
        if action == "list":
            return self.GetFleetList()

    def getPlanetName(self, relation, radar_strength, ownerName, planetName):
        if relation == rSelf:
            return planetName
        elif relation == rAlliance:
            return ownerName
        elif relation == rFriend:
            return ownerName
        else:
            if radar_strength > 0:
                return ownerName if ownerName else ""
            else:
                return ""

    # return if the given name if valid for a fleet, a planet
    def isValidCategoryName(self, name):
        name = name.strip()

        if name == "" or len(name) < 2 or len(name) > 32:
            return False
        else:
            p = re.compile("^[a-zA-Z0-9\- ]+$")
            return p.match(name)

    # List the fleets owned by the player
    def GetFleetList(self):

        content = GetTemplate(self.request, "s03/fleets-handler")

        query = "SELECT fleetid, fleets_ships.shipid, quantity" + \
                " FROM fleets" + \
                "    INNER JOIN fleets_ships ON (fleets.id=fleets_ships.fleetid)" + \
                " WHERE ownerid=" + str(self.UserId) + \
                " ORDER BY fleetid, fleets_ships.shipid"
        ShipListArray = oConnExecuteAll(query)

        query = "SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername," + \
                " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation," + \
                " destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_ownerid, destplanet_owner_name, destplanet_owner_relation," + \
                " cargo_capacity, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers," + \
                " recycler_output, orbit_ore > 0 OR orbit_hydrocarbon > 0, action," + \
                "( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.planet_galaxy AND nav_planet.sector = f.planet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = "+str(self.UserId)+")) AS from_radarstrength, " + \
                "( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.destplanet_galaxy AND nav_planet.sector = f.destplanet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = "+str(self.UserId)+")) AS to_radarstrength," + \
                " categoryid" + \
                " FROM vw_fleets as f WHERE ownerid=" + str(self.UserId)
        oRss = oConnExecuteAll(query)

        list = []
        content.AssignValue("fleets", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["id"] = oRs[0]
            item["name"] = oRs[1]
            item["category"] = oRs[37]
            item["size"] = oRs[4]
            item["signature"] = oRs[5]
            item["cargo_load"] = oRs[27]+oRs[28]+oRs[29]+oRs[30]+oRs[31]
            item["cargo_capacity"] = oRs[26]

            item["cargo_ore"] = oRs[27]
            item["cargo_hydrocarbon"] = oRs[28]
            item["cargo_scientists"] = oRs[29]
            item["cargo_soldiers"] = oRs[30]
            item["cargo_workers"] = oRs[31]

            item["commandername"] = oRs[9]
            item["action"] = abs(oRs[34])

            if oRs[3]: item["action"] = "x"

            if oRs[2]:
                item["stance"] = 1
            else:
                item["stance"] = 0

            if oRs[7]:
                item["time"] = oRs[7]
            else:
                item["time"] = 0

            # Assign fleet current planet
            item["planetid"] = 0
            item["g"] = 0
            item["s"] = 0
            item["p"] = 0
            item["relation"] = 0
            item["planetname"] = ""

            if (oRs[10]):
                item["planetid"] = oRs[10]
                item["g"] = oRs[12]
                item["s"] = oRs[13]
                item["p"] = oRs[14]
                item["relation"] = oRs[17]
                item["planetname"] = self.getPlanetName(oRs[17], oRs[35], oRs[16], oRs[11])

            # Assign fleet destination planet
            item["t_planetid"] = 0
            item["t_g"] = 0
            item["t_s"] = 0
            item["t_p"] = 0
            item["t_relation"] = 0
            item["t_planetname"] = ""

            if (oRs[18]):
                item["t_planetid"] = oRs[18]
                item["t_g"] = oRs[20]
                item["t_s"] = oRs[21]
                item["t_p"] = oRs[22]
                item["t_relation"] = oRs[25]
                item["t_planetname"] = self.getPlanetName(oRs[25], oRs[36], oRs[24], oRs[19])

            item['ships'] = []
            for ship in ShipListArray:
                if ship[0] == oRs[0]:
                    s = {}
                    item['ships'].append(s)
                    s["ship_label"] = getShipLabel(ship[1])
                    s["ship_quantity"] = ship[2]
                    
            item['resources'] = []
            
            res1 = {}
            res1["res_id"] = 1
            res1["res_quantity"] = oRs[27]
            item['resources'].append(res1)

            res2 = {}
            res2["res_id"] = 2
            res2["res_quantity"] = oRs[28]
            item['resources'].append(res2)

            res3 = {}
            res3["res_id"] = 3
            res3["res_quantity"] = oRs[29]
            item['resources'].append(res3)

            res4 = {}
            res4["res_id"] = 4
            res4["res_quantity"] = oRs[30]
            item['resources'].append(res4)

            res5 = {}
            res5["res_id"] = 5
            res5["res_quantity"] = oRs[31]
            item['resources'].append(res5)

        content.Parse("list")

        return render(self.request, content.template, content.data)
