# -*- coding: utf-8 -*-

from random import *

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "intelligence"

        self.nation_cost_lvl_0 = 250
        self.nation_cost_lvl_1 = 500
        self.nation_cost_lvl_2 = 1000
        self.nation_cost_lvl_3 = 2000

        self.fleets_cost_lvl_0 = 1000
        self.fleets_cost_lvl_1 = 5000
        self.fleets_cost_lvl_2 = 25000
        self.fleets_cost_lvl_3 = 65000

        self.planet_cost_lvl_0 = 50
        self.planet_cost_lvl_1 = 100
        self.planet_cost_lvl_2 = 200
        self.planet_cost_lvl_3 = 400

        self.e_no_error = 0
        self.e_general_error = 1
        self.e_not_enough_money = 2
        self.e_planet_not_exists = 3
        self.e_player_not_exists = 4
        self.e_own_nation_planet = 5

        self.intell_error = self.e_no_error

        #
        # process page
        #

        if self.SecurityLevel < 3:
            return HttpResponseRedirect("/")

        self.category = 8

        spotted = False

        action = request.POST.get("spy")
        self.level = ToInt(request.POST.get("level"), -1)

        if action == "nation":
            self.SpyNation()

        elif action == "planet":
            self.SpyPlanet()

        return self.DisplayIntelligence()

    def sqlValue(self, value):
        if value == None:
            sqlValue = "None"
        else:
            sqlValue = "'"+value+"'"

    #
    # display mercenary service page
    #
    def DisplayIntelligence(self):
        content = GetTemplate(self.request, "s03/mercenary-intelligence")

        # Assign service costs
        content.AssignValue("nation_cost_lvl_0", self.nation_cost_lvl_0)
        content.AssignValue("fleets_cost_lvl_0", self.fleets_cost_lvl_0)
        content.AssignValue("planet_cost_lvl_0", self.planet_cost_lvl_0)

        content.AssignValue("nation_cost_lvl_1", self.nation_cost_lvl_1)
        content.AssignValue("fleets_cost_lvl_1", self.fleets_cost_lvl_1)
        content.AssignValue("planet_cost_lvl_1", self.planet_cost_lvl_1)

        content.AssignValue("nation_cost_lvl_2", self.nation_cost_lvl_2)
        content.AssignValue("fleets_cost_lvl_2", self.fleets_cost_lvl_2)
        content.AssignValue("planet_cost_lvl_2", self.planet_cost_lvl_2)

        content.AssignValue("nation_cost_lvl_3", self.nation_cost_lvl_3)
        content.AssignValue("fleets_cost_lvl_3", self.fleets_cost_lvl_3)
        content.AssignValue("planet_cost_lvl_3", self.planet_cost_lvl_3)

        # display errors
        intell_type = self.request.POST.get("spy", "")

        if self.intell_error != self.e_no_error:
            content.Parse(str(intell_type) + "_error" + str(self.intell_error))
        else:
            content.Parse(str(intell_type) + "_ok")

        return self.Display(content)

    # action : type of order
    # self.level : self.level of the recruited spy, determine spottedChance and -Modifier values
    #  - spottedChance : chance that the spy has to be spotted per planet/fleet/building spied
    #  - getinfoModifier : chance that the spy retrieve common info
    #  - getmoreModifier : chance the the spy retrieve rare info
    # spotted : set to True if spy has been spotted
    # id : spied user id
    # nation : spied user name

    # self.category : intelligence self.category id for reports.asp
    # type : action id for reports.asp
    # cost : action cost ; determined by action + self.level

    #
    # Retrieve info about a nation
    #
    def SpyNation(self):
        typ = 1

        nation = self.request.POST.get("nation_name", "")
        oRs = oConnExecute("SELECT id FROM users WHERE (privilege=-2 OR privilege=0) AND upper(login) = upper(" + dosql(nation) + ")")
        if oRs == None:
            self.intell_error = self.e_player_not_exists
            return
        else:
            id = oRs[0]
            if id == self.UserId:
                self.intell_error = self.e_own_nation_planet
                return

        #
        # Begin transaction
        #
        oRs = oConnExecute("SELECT sp_create_spy('" + str(self.UserId) + "', int2(" + str(typ) + "), int2(" + str(self.level) + ") )")
        reportid = oRs[0]
        if reportid < 0:
            self.intell_error = self.e_general_error
            return

        oConnDoQuery("UPDATE spy SET target_name=sp_get_user(" + str(id) + ") WHERE id=" + str(reportid))

        nb_planet = 0

        if self.level == 0:
            planet_limit = 5

            spottedChance = 0.6
            getinfoModifier = 0.10
            cost = self.nation_cost_lvl_0
            spyingTime = 25
        elif self.level == 1:
            planet_limit = 15

            spottedChance = 0.3
            getinfoModifier = 0.05
            cost = self.nation_cost_lvl_1
            spyingTime = 30
        elif self.level == 2:
            planet_limit = 0 # no limit

            spottedChance = 0.15
            getinfoModifier = 0.01
            cost = self.nation_cost_lvl_2
            spyingTime = round(60 + random() * 30)
        elif self.level == 3:
            planet_limit = 0 # means no limit

            spottedChance = 0
            getinfoModifier = 0
            cost = self.nation_cost_lvl_3
            spyingTime = round(300 + random() * 150)

        if self.oPlayerInfo["prestige_points"] < cost:
            self.intell_error = self.e_not_enough_money
            return

        # test is the spy is spotted
        spotted = random() < spottedChance

        #
        # retrieve nation planet list and fill report
        #
        query = " SELECT id, name, floor, space, pct_ore, pct_hydrocarbon," + \
                    " COALESCE((SELECT SUM(quantity*signature) " + \
                    " FROM planet_ships " + \
                    " LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id) " + \
                    " WHERE planet_ships.planetid=vw_planets.id),0) " + \
                " FROM vw_planets " + \
                " WHERE ownerid=" + str(id) + \
                " ORDER BY random() "
        oRss = oConnExecuteAll(query)
        for oRs in oRss:
            # test if info is retrieved by the spy (failure probability increase for each new info)
            if planet_limit == 0 or nb_planet < planet_limit:
                # add planet to the spy report
                query = " INSERT INTO spy_planet(spy_id,  planet_id,  planet_name,  floor,  space, pct_ore, pct_hydrocarbon,  ground) " + \
                        " VALUES("+ str(reportid) +"," + str(oRs[0]) +"," + dosql(oRs[1]) +"," + str(oRs[2]) + "," + str(oRs[3]) + "," + str(oRs[4]) + "," + str(oRs[5]) + "," + str(oRs[6]) +")"
                oConnDoQuery(query)

                nb_planet = nb_planet + 1

        #
        # For veteran spy, collect additionnal research infos
        #
        if self.level >= 2:
            query = " SELECT researchid, level " + \
                    " FROM sp_list_researches(" + str(id) + ") " + \
                    " WHERE level > 0" + \
                    " ORDER BY researchid "
            oRss = oConnExecuteAll(query)

            for oRs in oRss:
                # add research info to spy report
                query = " INSERT INTO spy_research(spy_id,  research_id,  research_level) " + \
                        " VALUES("+ str(reportid) +", " + str(oRs[0]) +", " + str(oRs[1]) +") "
                oConnDoQuery(query)

        #
        # Add spy reports in report list
        #
        query = " INSERT INTO reports(ownerid, type, subtype, datetime, spyid, description) " + \
                " VALUES(" + str(self.UserId) + ", " + str(self.category) + ", " + str(typ*10) + ", now() + " + str(spyingTime + nb_planet) + "*interval '1 minute', " + str(reportid) + ", sp_get_user(" + str(id) + ")) "

        oConnDoQuery(query)

        if spotted and self.request.session.get("privilege", 0) < 100:
            # update report if spy has been spotted
            query = " UPDATE spy " + \
                    " SET spotted=" + str(spotted) + \
                    " WHERE id=" + str(reportid) + " AND userid=" + str(self.UserId)
            oConnDoQuery(query)

            # add report in spied nation's report list
            query = " INSERT INTO reports(ownerid, type, subtype, datetime, spyid, description) " + \
                    " VALUES(" + str(id) + ", " + str(self.category) + ", " + str(typ) + ", now() + " + str(spyingTime + nb_planet) + "*interval '40 seconds', " + str(reportid) + ", sp_get_user(" + str(self.UserId) + ")) "

            oConnDoQuery(query)

        #
        # withdraw the operation cost from player's account
        #
        query = "UPDATE users SET prestige_points=prestige_points - " + str(cost) + " WHERE id=" + str(self.UserId)

        oConnDoQuery(query)

    #
    # Retrieve info about a planet
    #
    def SpyPlanet(self):

        g = ToInt(self.request.POST.get("g"), 0)
        s = ToInt(self.request.POST.get("s"), 0)
        p = ToInt(self.request.POST.get("p"), 0)

        typ = 3

        if self.request.session.get("privilege", 0) < 100:

            oRs = oConnExecute("SELECT ownerid FROM nav_planet WHERE galaxy=" + str(g) + " AND sector=" + str(s) + " AND planet=" + str(p))
    
            if oRs == None:
                self.intell_error = self.e_planet_not_exists
                return
            elif oRs[0] == self.UserId:
                self.intell_error = self.e_own_nation_planet
                return

        #
        # Begin transaction
        #
        oRs = oConnExecute("SELECT sp_create_spy('" + str(self.UserId) + "', int2(" + str(typ) + "), int2(" + str(self.level) + ") )")
        reportid = oRs[0]
        if reportid < 0:
            self.intell_error = self.e_general_error
            return

        if self.level == 0:
            spottedChance = 0.6
            getinfoModifier = 0.05
            cost = self.planet_cost_lvl_0
            spyingTime = 5
        elif self.level == 1:
            spottedChance = 0.3
            getinfoModifier = 0.025
            cost = self.planet_cost_lvl_1
            spyingTime = 10
        elif self.level == 2:
            spottedChance = 0.15
            getinfoModifier = 0
            cost = self.planet_cost_lvl_2
            spyingTime = round(20 + random() * 10)
        elif self.level == 3:
            spottedChance = 0
            getinfoModifier = 0
            cost = self.planet_cost_lvl_3
            spyingTime = round(100 + random() * 50)

        if self.oPlayerInfo["prestige_points"] < cost:
            self.intell_error = self.e_not_enough_money
            return

        # retrieve planet info list
        query = " SELECT id, name, ownerid, sp_get_user(ownerid), floor, space, floor_occupied, space_occupied,  " + \
                    " COALESCE((SELECT SUM(quantity*signature) " + \
                    " FROM planet_ships " + \
                    " LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id) " + \
                    " WHERE planet_ships.planetid=vw_planets.id),0), " + \
                " ore, hydrocarbon, ore_capacity, hydrocarbon_capacity, ore_production, hydrocarbon_production, " + \
                " energy_consumption, energy_production, " + \
                " radar_strength, radar_jamming, colonization_datetime, orbit_ore, orbit_hydrocarbon, " + \
                " workers, workers_capacity, scientists, scientists_capacity, soldiers, soldiers_capacity, " + \
                " pct_ore, pct_hydrocarbon" + \
                " FROM vw_planets " + \
                " WHERE galaxy=" + str(g) + " AND sector=" + str(s) + " AND planet=" + str(p)

        oRs = oConnExecute(query)
        if oRs == None:
            self.intell_error = self.e_planet_not_exists
            return

        # test is the spy is spotted
        spotted = random() < spottedChance

        if oRs:

            planet = oRs[0]

            if self.request.session.get("privilege", 0) > 100: return

            if oRs[2]:
            #
            # somebody owns this planet, so the spy can retrieve several info on it
            #
                # retrieve ownerid and planetname
                id = oRs[2]
                if oRs[1]:
                    planetname = dosql(oRs[1])
                else:
                    planetname = "''"

                # set the owner of the planet as the target nation
                oConnDoQuery("UPDATE spy SET target_name=sp_get_user(" + str(id) + ") WHERE id=" + str(reportid))

                # basic info retrieved by all spies
                query = " INSERT INTO spy_planet(spy_id,  planet_id,  planet_name, owner_name, floor, space, pct_ore, pct_hydrocarbon, ground ) " + \
                        " VALUES ("+ str(reportid) +", " + sqlValue(oRs[0]) + "," + sqlValue(planetname) +"," + dosql(oRs[3]) +"," + \
                        sqlValue(oRs[4]) + "," + sqlValue(oRs[5]) + "," + sqlValue(oRs[28]) + "," + sqlValue(oRs[29]) + "," + sqlValue(oRs[8]) + ")"

                oConnDoQuery(query)

                # common info retrieved by spies which self.level >= 0 (actually, all)
                if self.level >= 0:
                    query = " UPDATE spy_planet SET"+ \
                            " radar_strength=" + sqlValue(oRs[17]) + ", radar_jamming=" + sqlValue(oRs[18]) + ", " + \
                            " orbit_ore=" + sqlValue(oRs[20]) + ", orbit_hydrocarbon=" + sqlValue(oRs[21]) + \
                            " WHERE spy_id=" + str(reportid) + " AND planet_id=" + sqlValue(oRs[0])

                    oConnDoQuery(query)

                # uncommon info retrieved by skilled spies with self.level >= 1 : ore, hydrocarbon, energy
                if self.level >= 1:
                    query = "UPDATE spy_planet SET"+ \
                            " ore=" + sqlValue(oRs[9]) + ", hydrocarbon=" + sqlValue(oRs[10]) + \
                            ", ore_capacity=" + sqlValue(oRs[11]) + ", hydrocarbon_capacity=" + sqlValue(oRs[12]) + \
                            ", ore_production=" + sqlValue(oRs[13]) + ", hydrocarbon_production=" + sqlValue(oRs[14]) + \
                            ", energy_consumption=" + sqlValue(oRs[15]) + ", energy_production=" + sqlValue(oRs[16]) + \
                            " WHERE spy_id=" + str(reportid) + " AND planet_id=" + sqlValue(oRs[0])

                    oConnDoQuery(query)

                if self.level >= 2:
                    #
                    # rare info that can be retrieved by veteran spies only : workers, scientists, soldiers
                    #
                    query = "UPDATE spy_planet SET"+ \
                            " workers=" + sqlValue(oRs[22]) + ", workers_capacity=" + sqlValue(oRs[23]) + ", " + \
                            " scientists=" + sqlValue(oRs[24]) + ", scientists_capacity=" + sqlValue(oRs[25]) + ", " + \
                            " soldiers=" + sqlValue(oRs[26]) + ", soldiers_capacity=" + sqlValue(oRs[27]) + \
                            " WHERE spy_id=" + str(reportid) + " AND planet_id=" + sqlValue(oRs[0])

                    oConnDoQuery(query)

                    #
                    # Add the buildings of the planet under construction
                    #
                    query = "SELECT planetid, id, build_status, quantity, construction_maximum " + \
                            " FROM vw_buildings AS b " + \
                            " WHERE planetid=" + str(planet) + " AND build_status IS NOT NULL"

                    oRss = oConnExecuteAll(query)
                    i = 0
                    for oRs in oRss:
                        
                        rand1 = random()

                        # test if info is correctly retrieved by the spy (error probability increase for each new info)
                        qty = oRs[3]

                        if rand1 < ( getinfoModifier * i ) and oRs[4] != 1:
                            # if construction_maximum = 1: error is impossible : if there is 1 city, it can't exists more or less
                            # info are always retrieved, but the spy may give a wrong number of constructions ( actually right number +/- 50% )

                            # calculate maximum and minimum possible numbers of buildings
                            rndmax = int(oRs[3]*1.5)
                            if rndmax <= oRs[3]: rndmax = rndmax + 1
                            rndmax = min(rndmax, oRs[4])
                            rndmin = int(oRs[3]*0.5)
                            if rndmin < 1: rndmin = 1
                            qty = int((rndmax-rndmin+1)*random()+rndmin)

                        query = "INSERT INTO spy_building(spy_id, planet_id, building_id, endtime, quantity) " + \
                                " VALUES (" + str(reportid) + ", " + str(oRs[0]) + ", " + str(oRs[1]) + ", now() + " + str(oRs[2]) + "* interval '1 second', " + str(qty) + " )"

                        oConnDoQuery(query)
                        i += 1

                if self.level >= 0:

                    #
                    # Add the buildings of the planet
                    #
                    query = "SELECT planetid, id, quantity, construction_maximum" + \
                            " FROM vw_buildings" + \
                            " WHERE planetid=" + str(planet) + " AND quantity != 0 AND build_status IS NULL AND destruction_time IS NULL"
                    oRss = oConnExecuteAll(query)
                    i = 0
                    for oRs in oRss:

                        rand1 = random()

                        # test if info is correctly retrieved by the spy (error probability increase for each new info)
                        qty = oRs[2]

                        if rand1 < ( getinfoModifier * i ) and oRs[3] != 1:
                            # if construction_maximum = 1: error is impossible : if there is 1 city, it can't exists more or less
                            # info are always retrieved, but the spy may give a wrong number of constructions ( actually right number +/- 50% )

                            # calculate maximum and minimum possible numbers of buildings
                            rndmax = int(oRs[2]*1.5)
                            if rndmax <= oRs[2]: rndmax = rndmax + 1
                            rndmax = min(rndmax, oRs[3])
                            rndmin = int(oRs[2]*0.5)
                            if rndmin < 1: rndmin = 1
                            qty = int((rndmax-rndmin+1)*random()+rndmin)

                        query = " INSERT INTO spy_building(spy_id, planet_id, building_id, quantity) " + \
                                " VALUES(" + str(reportid) + ", " + str(oRs[0]) + ", " + str(oRs[1]) + ", " + str(qty) + " )"

                        oConnDoQuery(query)
                        
                        i += 1

            else:
                #
                # nobody own this planet
                #
                query = " INSERT INTO spy_planet(spy_id, planet_id, floor, space) " + \
                        " VALUES("+ str(reportid) +", " + sqlValue(oRs[0]) +", " + sqlValue(oRs[4]) +", " + sqlValue(oRs[5]) +") "
                oConnDoQuery(query)
                return

        #
        # Add spy reports in report list
        #
        query = " INSERT INTO reports(ownerid, type, subtype, datetime, spyid, planetid) " + \
                " VALUES(" + str(self.UserId) + ", " + str(self.category) + ", " + str(typ*10) + ", now()+" + str(spyingTime) + "*interval '1 minute', " + str(reportid) + ", " + str(planet) + ") "

        oConnDoQuery(query)

        # update report if spy has been spotted
        if spotted and self.request.session.get("privilege", 0) < 100:
            query = "UPDATE spy SET" + \
                    " spotted=" + str(spotted) + \
                    " WHERE id=" + str(reportid) + " AND userid=" + str(self.UserId)

            oConnDoQuery(query)

            # add report in spied nation's report list
            query = " INSERT INTO reports(ownerid, type, subtype, datetime, spyid, planetid, description) " + \
                    " VALUES(" + str(id) + "," + str(self.category) + "," + str(typ) + ", now()+" + str(spyingTime) + "*interval '40 seconds'," + str(reportid) + "," + str(planet) + ", sp_get_user(" + str(self.UserId) + "))"

            oConnDoQuery(query)

        #
        # withdraw the operation cost from player's account
        #
        query = "UPDATE users SET prestige_points = prestige_points - " + str(cost) + " WHERE id=" + str(self.UserId)

        oConnDoQuery(query)
