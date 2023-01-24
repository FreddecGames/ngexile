# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "intelligence"

        self.id = request.GET.get("id", "")
        if self.id == "":
            return HttpResponseRedirect("/s03/reports/")

        self.id = int(self.id)

        key = request.GET.get("key", "")
        if key == "":
            return HttpResponseRedirect("/s03/reports/")

        #
        # retrieve report id and info
        #

        query = "SELECT id, key, userid, type, level, date, credits, spotted, target_name" + \
                " FROM spy" + \
                " WHERE id="+str(self.id)+" AND key="+dosql(key)

        oRs = oConnExecute(query)

        # check if report exists and if given key is correct otherwise redirect to the reports
        if oRs == None:
            return HttpResponseRedirect("/s03/reports/")

        else:
            #user = oRs[2]
            typ = oRs[3]
            self.level = oRs[4]
            self.spydate = oRs[5]

            self.credits = oRs[6]
            self.spotted = oRs[7]
            if oRs[8]: self.target = oRs[8]

        if typ == 1:
            return self.DisplayNation()
        elif typ == 3:
            return self.DisplayPlanet()
        else:
            return HttpResponseRedirect("/s03/reports/")

    #
    # display the spy report of a nation
    #
    def DisplayNation(self):

        # load template
        content = GetTemplate(self.request, "s03/spy-report")

        #
        # list spied planets
        #
        query = " SELECT spy_id, planet_id, planet_name, spy_planet.floor, spy_planet.space, ground, galaxy, sector, planet, spy_planet.pct_ore, spy_planet.pct_hydrocarbon " + \
                " FROM spy_planet " + \
                " LEFT JOIN nav_planet " + \
                    " ON ( spy_planet.planet_id=nav_planet.id) " + \
                " WHERE spy_id=" + str(self.id)

        oRss = oConnExecuteAll(query)

        nbplanet = 0

        list = []
        content.AssignValue("planets", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            if oRs[2]:
                item["planet"] = oRs[2]
            else:
                item["planet"] = target

            item["g"] = oRs[6]
            item["s"] = oRs[7]
            item["p"] = oRs[8]

            item["floor"] = oRs[3]
            item["space"] = oRs[4]
            item["ground"] = oRs[5]

            item["pct_ore"] = oRs[9]
            item["pct_hydrocarbon"] = oRs[10]

            nbplanet = nbplanet + 1

        #
        # list spied technologies
        #
        query = " SELECT category, db_research.id, research_level, levels " + \
                " FROM spy_research " + \
                " LEFT JOIN db_research " + \
                    " ON ( spy_research.research_id=db_research.id) " + \
                " WHERE spy_id=" + str(self.id)  + \
                " ORDER BY category, db_research.id "

        oRss = oConnExecuteAll(query)

        nbresearch = 0

        lastCategory = -1

        cats = []
        for oRs in oRss:

            category = oRs[0]

            if category != lastCategory:
                cat = { "list":[] }
                cat["id"] = category
                lastCategory = category
                itemCount = 0

            itemCount = itemCount + 1

            item = {}
            item["research"] = getResearchLabel(oRs[1])
            item["level"] = oRs[2]
            item["levels"] = oRs[3]

            nbresearch = nbresearch + 1

            cat["list"].append(item)

        # display spied nation credits if possible
        if self.credits:
            content.AssignValue("credits", self.credits)
            content.Parse("credits")

        if nbresearch != 0:
            content.AssignValue("nb_research", nbresearch)
            content.Parse("researches")

        content.AssignValue("date", self.spydate)
        content.AssignValue("nation", self.target)
        content.AssignValue("nb_planet", nbplanet)
        content.AssignValue("level", self.level)

        # spotted is True if our spy has been spotted while he was doing his job
        if self.spotted: content.Parse("spotted")

        content.Parse("spynation")

        return self.Display(content)

    def DisplayPlanet(self):
        content = GetTemplate(self.request, "s03/spy-report")

        query = " SELECT spy_id,  planet_id,  planet_name,  s.owner_name,  s.floor,  s.space,  s.ground,  s.ore,  s.hydrocarbon,  s.ore_capacity, " + \
                " s.hydrocarbon_capacity,  s.ore_production,  s.hydrocarbon_production,  s.energy_consumption,  s.energy_production,  s.workers,  s.workers_capacity,  s.scientists, " + \
                " s.scientists_capacity,  s.soldiers,  s.soldiers_capacity,  s.radar_strength,  s.radar_jamming,  s.orbit_ore,  " + \
                " s.orbit_hydrocarbon, galaxy, sector, planet, s.pct_ore, s.pct_hydrocarbon " + \
                " FROM spy_planet AS s" + \
                " LEFT JOIN nav_planet " + \
                    " ON ( s.planet_id=nav_planet.id) " + \
                " WHERE spy_id=" + str(self.id)

        oRs = oConnExecute(query)

        if oRs == None:
            return HttpResponseRedirect("/s03/reports/")

        planet = oRs[1]

        # display basic info
        content.AssignValue("name", oRs[2])
        content.AssignValue("location", str(oRs[25]) + ":" + str(oRs[26]) + ":" + str(oRs[27]))
        content.AssignValue("floor", oRs[4])
        content.AssignValue("space", oRs[5])
        content.AssignValue("ground", oRs[6])

        content.AssignValue("pct_ore", oRs[28])
        content.AssignValue("pct_hydrocarbon", oRs[29])

        if oRs[3]:
            content.AssignValue("owner", oRs[3])
        else:
            content.Parse("no_owner")

        if oRs[7]: # display common info
            content.AssignValue("ore", oRs[7])
            content.AssignValue("hydrocarbon", oRs[8])
            content.AssignValue("ore_capacity", oRs[9])
            content.AssignValue("hydrocarbon_capacity", oRs[10])
            content.AssignValue("ore_prod", oRs[11])
            content.AssignValue("hydrocarbon_prod", oRs[12])
            content.AssignValue("energy_consumption", oRs[13])
            content.AssignValue("energy_prod", oRs[14])
            content.Parse("common")

        if oRs[15]: # display rare info
            content.AssignValue("workers", oRs[15])
            content.AssignValue("workers_cap", oRs[16])
            content.AssignValue("scientists", oRs[17])
            content.AssignValue("scientists_cap", oRs[18])
            content.AssignValue("soldiers", oRs[19])
            content.AssignValue("soldiers_cap", oRs[20])
            content.Parse("rare")

        if oRs[21]: # display uncommon info
            content.AssignValue("radar_strength", oRs[21])
            content.AssignValue("radar_jamming", oRs[22])
            content.AssignValue("orbit_ore", oRs[23])
            content.AssignValue("orbit_hydrocarbon", oRs[24])
            content.Parse("uncommon")

        # display pending buildings
        query = " SELECT s.building_id, s.quantity, label, s.endtime, category " + \
                " FROM spy_building AS s " + \
                " LEFT JOIN db_buildings " + \
                    " ON (s.building_id=id) " + \
                " WHERE spy_id=" + str(self.id) + " AND planet_id=" + str(planet) + " AND s.endtime IS NOT NULL " + \
                " ORDER BY category, label "

        oRss = oConnExecuteAll(query)

        if oRss:
            list = []
            content.AssignValue("buildings_pendings", list)
            for oRs in oRss:
                item = {}
                list.append(item)
                
                item["building"] = oRs[2]
                item["qty"] = oRs[1]
                item["endtime"] = oRs[3]

        # display built buildings
        query = " SELECT s.building_id, s.quantity, label, s.endtime, category " + \
                " FROM spy_building AS s " + \
                " LEFT JOIN db_buildings " + \
                    " ON (s.building_id=id) " + \
                " WHERE spy_id=" + str(self.id) + " AND planet_id=" + str(planet) + " AND s.endtime IS NULL " + \
                " ORDER BY category, label "

        oRss = oConnExecuteAll(query)

        if oRss:
            list = []
            content.AssignValue("buildings", list)
            for oRs in oRss:
                item = {}
                list.append(item)
                
                item["building"] = oRs[2]
                item["qty"] = oRs[1]

        content.AssignValue("date", self.spydate)
        content.AssignValue("nation", self.target)

        content.AssignValue("level", self.level)

        # spotted is True if our spy has been spotted while he was doing his job
        if self.spotted: content.Parse("spotted")

        content.Parse("spyplanet")

        return self.Display(content)
