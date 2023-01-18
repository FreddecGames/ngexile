from .base import *


class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "planet"

        self.showHeader = True

        e_no_error = 0
        self.e_rename_bad_name = 1

        self.planet_error = e_no_error

        if request.POST.get("action") == "assigncommander":
            if toInt(request.POST.get("commander"), 0) != 0: # assign selected commander
                query = "SELECT * FROM sp_commanders_assign(" + str(self.profile['id']) + "," + str(toInt(request.POST.get("commander"), 0)) + "," + str(self.currentPlanet['id']) + ",null)"
                dbQuery(query)
            else:
                # unassign current planet commander
                query = "UPDATE nav_planet SET commanderid=null WHERE ownerid=" + str(self.profile['id']) + " AND id=" + str(self.currentPlanet['id'])
                dbQuery(query)

        elif request.POST.get("action") == "rename":
            if not isValidObjectName(request.POST.get("name")):
                self.planet_error = self.e_rename_bad_name
            else:
                query = "UPDATE nav_planet SET name=" + strSql(request.POST.get("name")) + \
                        " WHERE ownerid=" + str(self.profile['id']) + " AND id=" + str(self.currentPlanet['id'])

                dbQuery(query)

        elif request.POST.get("action") == "firescientists":
            amount = toInt(request.POST.get("amount"), 0)
            oConnExecute("SELECT sp_dismiss_staff(" + str(self.profile['id']) + "," + str(self.currentPlanet['id']) + "," + str(amount) + ",0,0)")
        elif request.POST.get("action") == "firesoldiers":
            amount = toInt(request.POST.get("amount"), 0)
            oConnExecute("SELECT sp_dismiss_staff(" + str(self.profile['id']) + "," + str(self.currentPlanet['id']) + "," + "0," + str(amount) + ",0)")
        elif request.POST.get("action") == "fireworkers":
            amount = toInt(request.POST.get("amount"), 0)
            oConnExecute("SELECT sp_dismiss_staff(" + str(self.profile['id']) + "," + str(self.currentPlanet['id']) + "," + "0,0," + str(amount) + ")")

        elif request.POST.get("action") == "abandon":
            oConnExecute("SELECT sp_abandon_planet(" + str(self.profile['id']) + "," + str(self.currentPlanet['id']) + ")")
            return HttpResponseRedirect("/s03/empire-view/")

        elif request.POST.get("action") == "resources_price":
            query = "UPDATE nav_planet SET" + \
                    " buy_ore = GREATEST(0, LEAST(1000, " + str(toInt(request.POST.get("buy_ore"), 0)) + "))" + \
                    " ,buy_hydrocarbon = GREATEST(0, LEAST(1000, " + str(toInt(request.POST.get("buy_hydrocarbon"), 0)) + "))" + \
                    " WHERE ownerid=" + str(self.profile['id']) + " AND id=" + str(self.currentPlanet['id'])
            dbQuery(query)

        if request.GET.get("a") == "suspend":
            oConnExecute("SELECT sp_update_planet_production(" + str(self.currentPlanet['id']) + ")")
            dbQuery("UPDATE nav_planet SET mod_production_workers=0, recruit_workers=False WHERE ownerid=" + str(self.profile['id']) + " AND id=" + str(self.currentPlanet['id']) )
        elif request.GET.get("a")== "resume":
            dbQuery("UPDATE nav_planet SET recruit_workers=True WHERE ownerid=" + str(self.profile['id']) + " AND id=" + str(self.currentPlanet['id']) )
            oConnExecute("SELECT sp_update_planet(" + str(self.currentPlanet['id']) + ")")

        return self.DisplayPlanet()

    def DisplayPlanet(self):

        content = getTemplateContext(self.request, "planet-view")

        CmdReq=""

        query = "SELECT id, name, galaxy, sector, planet, " + \
                "floor_occupied, floor, space_occupied, space, workers, workers_capacity, mod_production_workers," + \
                "scientists, scientists_capacity, soldiers, soldiers_capacity, commanderid, recruit_workers," + \
                "planet_floor, COALESCE(buy_ore, 0), COALESCE(buy_hydrocarbon, 0)," + \
                "credits_production, credits_random_production, production_prestige," + \
                "upkeep, workers_for_maintenance" + \
                " FROM vw_planets WHERE id=" + str(self.currentPlanet['id'])

        oRs = oConnExecute(query)

        if oRs:
            content.assignValue("planet_id", oRs[0])
            content.assignValue("planet_name", oRs[1])
            content.assignValue("planet_img", getPlanetImg(oRs[0], oRs[18]))

            content.assignValue("pla_g", oRs[2])
            content.assignValue("pla_s", oRs[3])
            content.assignValue("pla_p", oRs[4])

            content.assignValue("floor_occupied", oRs[5])
            content.assignValue("floor", oRs[6])

            content.assignValue("space_occupied", oRs[7])
            content.assignValue("space", oRs[8])

            content.assignValue("workers", oRs[9])
            content.assignValue("workers_capacity", oRs[10])

            content.assignValue("scientists", oRs[12])
            content.assignValue("scientists_capacity", oRs[13])

            content.assignValue("soldiers", oRs[14])
            content.assignValue("soldiers_capacity", oRs[15])

            content.assignValue("growth", oRs[11]/10)

            if oRs[17]:
                content.parse("suspend")
            else:
                content.parse("resume")

            content.assignValue("buy_ore", oRs[19])
            content.assignValue("buy_hydrocarbon", oRs[20])

            # retrieve commander assigned to this planet
            if oRs[16]:
                oCmdRs = oConnExecute("SELECT name FROM commanders WHERE ownerid="+str(self.profile['id'])+" AND id="+str(oRs[16]))
                content.assignValue("commandername", oCmdRs[0])
                CmdId = oRs[16]
                content.parse("commander")
            else:
                content.parse("nocommander")
                CmdId = 0
                
            content.assignValue("credit_prod", int(oRs[21] + (oRs[22] / 2)))
            content.assignValue("prestige_prod", oRs[23])

            content.assignValue("upkeep_credits", oRs[24])
            content.assignValue("upkeep_workers", oRs[25])
            content.assignValue("upkeep_soldiers", int((oRs[9] + oRs[12]) / 250))

        if CmdId == 0: # display "no commander" or "fire commander"
            content.parse("none")
        else:
            content.parse("unassign")

        # display commmanders

        query = " SELECT id, name, fleetname, planetname, fleetid " + \
                " FROM vw_commanders" + \
                " WHERE ownerid="+str(self.profile['id']) + \
                " ORDER BY fleetid IS NOT NULL, planetid IS NOT NULL, fleetid, planetid "
        oRss = oConnExecuteAll(query)

        lastItem = ""
        item = ""
        ShowGroup = False

        cmd_groups = []
        content.assignValue("optgroups", cmd_groups)
        
        cmd_nones = {'typ':'none', 'cmds':[]}
        cmd_fleets = {'typ':'fleet', 'cmds':[]}
        cmd_planets = {'typ':'planet', 'cmds':[]}
        
        for oRs in oRss:
            item = {}

            if oRs[2] == None and oRs[3] == None:
                typ = "none"
                cmd_nones['cmds'].append(item)
            elif oRs[2] == None:
                typ = "planet"
                cmd_planets['cmds'].append(item)
            else:
                typ = "fleet"
                cmd_fleets['cmds'].append(item)

            if CmdId == oRs[0]: item["selected"] = True
            item["cmd_id"] = oRs[0]
            item["cmd_name"] = oRs[1]
            if typ == "planet":
                item["name"] = oRs[3]
                item["assigned"] = True

            if item == "fleet":
                item["name"] = oRs[2]
                activityRs = oConnExecute("SELECT dest_planetid, engaged, action FROM fleets WHERE ownerid="+str(self.profile['id'])+" AND id="+str(oRs[4]))
                if activityRs[0] == None and (not activityRs[1]) and activityRs[2]==0:
                    item["assigned"] = True
                else:
                    item["unavailable"] = True
                    
        if len(cmd_nones['cmds']) > 0: cmd_groups.append(cmd_nones)
        if len(cmd_fleets['cmds']) > 0: cmd_groups.append(cmd_fleets)
        if len(cmd_planets['cmds']) > 0: cmd_groups.append(cmd_planets)

        # view current buildings constructions
        query = "SELECT buildingid, remaining_time, destroying" + \
                " FROM vw_buildings_under_construction2 WHERE planetid="+str(self.currentPlanet['id']) + \
                " ORDER BY remaining_time DESC"

        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.assignValue("buildings", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["buildingid"] = oRs[0]
            item["building"] = getBuildingLabel(oRs[0])
            item["time"] = oRs[1]

            if oRs[2]: item["destroy"] = True

            i = i + 1

        if i==0: content.parse("nobuilding")

        query = "SELECT shipid, remaining_time, recycle" + \
                " FROM vw_ships_under_construction" + \
                " WHERE ownerid=" + str(self.profile['id']) + " AND planetid=" + str(self.currentPlanet['id']) + " AND end_time IS NOT NULL" + \
                " ORDER BY remaining_time DESC"

        # view current ships constructions
        oRss = oConnExecuteAll(query)

        i = 0

        list = []
        content.assignValue("ships", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["shipid"] = oRs[0]
            item["ship"] = getShipLabel(oRs[0])
            item["time"] = oRs[1]

            if oRs[2]: item["recycle"] = True

            i = i + 1

        if i==0: content.parse("noship")

        # list the fleets near the planet
        query = "SELECT id, name, attackonsight, engaged, size, signature, commanderid, (SELECT name FROM commanders WHERE id=commanderid) as commandername," + \
                " action, sp_relation(ownerid, " + str(self.profile['id']) + ") AS relation, sp_get_user(ownerid) AS ownername" + \
                " FROM fleets" + \
                " WHERE action != -1 AND action != 1 AND planetid=" + str(self.currentPlanet['id']) + \
                " ORDER BY upper(name)"

        oRss = oConnExecuteAll(query)

        i = 0

        list = []
        content.assignValue("fleets", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["id"] = oRs[0]
            item["size"] = oRs[4]
            item["signature"] = oRs[5]

            if oRs[9] > rFriend:
                item["name"] = oRs[1]
            else:
                item["name"] = oRs[10]

            if oRs[6]:
                item["commanderid"] = oRs[6]
                item["commandername"] = oRs[7]
                item["commander"] = True
            else:
                item["nocommander"] = True

            if oRs[3]:
                item["fighting"] = True
            elif oRs[8] == 2:
                item["recycling"] = True
            else:
                item["patrolling"] = True

            if oRs[9] in [rHostile, rWar]:
                item["enemy"] = True
            elif oRs[9] == rFriend:
                item["friend"] = True
            elif oRs[9] == rAlliance:
                item["ally"] = True
            elif oRs[9] == rSelf:
                item["owner"] = True

            i = i + 1

        if i==0: content.parse("nofleet")

        if self.planet_error == self.e_rename_bad_name:
                content.parse("rename_bad_name")

        content.parse("ondev")

        return self.display(content)
