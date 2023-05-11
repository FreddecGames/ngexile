# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        self.nation_cost_lvl_0 = 250
        self.nation_cost_lvl_1 = 500
        self.nation_cost_lvl_2 = 1000
        self.nation_cost_lvl_3 = 2000

        self.planet_cost_lvl_0 = 50
        self.planet_cost_lvl_1 = 100
        self.planet_cost_lvl_2 = 200
        self.planet_cost_lvl_3 = 400
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    ################################################################################
    
    def post(self, request, *args, **kwargs):

        #---
        
        action = request.POST.get("spy")
        
        #---
        
        if action == "nation":
            
            #---
            
            level = ToInt(request.POST.get("level"), -1)
            spotted = False
            category = 8
            
            #---
            
            nation = request.POST.get("nation_name", "")
            
            userId = dbExecute("SELECT id FROM users WHERE (privilege=-2 OR privilege=0) AND upper(username) = upper(" + dosql(nation) + ")")
            if userId == None:
                
                messages.error(request, 'player_not_exists')
                return HttpResponseRedirect(request.build_absolute_uri())
                
            elif userId == self.userId:
                
                messages.error(request, 'own_nation_planet')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            #---
            
            reportId = dbExecute("SELECT sp_create_spy('" + str(self.userId) + "', int2(" + str(1) + "), int2(" + str(level) + ") )")
            if reportId < 0:
                messages.error(request, 'general_error')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            #---
            
            dbQuery("UPDATE spy SET target_name=sp_get_user(" + str(userId) + ") WHERE id=" + str(reportId))

            #---
            
            if level == 0:
            
                planet_limit = 5
                spottedChance = 0.6
                cost = self.nation_cost_lvl_0
                spyingTime = 25
                
            elif level == 1:
            
                planet_limit = 15
                spottedChance = 0.3
                cost = self.nation_cost_lvl_1
                spyingTime = 30
                
            elif level == 2:
            
                planet_limit = 0
                spottedChance = 0.15
                cost = self.nation_cost_lvl_2
                spyingTime = round(60 + random() * 30)
                
            elif level == 3:
            
                planet_limit = 0
                spottedChance = 0
                cost = self.nation_cost_lvl_3
                spyingTime = round(300 + random() * 150)

            #---
            
            if self.profile["prestige_points"] < cost:
                messages.error(request, 'not_enough_money')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            #---
            
            nb_planet = 0
            
            query = "SELECT id, name, floor, space, pct_ore, pct_hydrocarbon," + \
                        " COALESCE((SELECT SUM(quantity*signature) " + \
                        " FROM planet_ships " + \
                        " LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id) " + \
                        " WHERE planet_ships.planetid=vw_planets.id),0) AS ground" + \
                    " FROM vw_planets" + \
                    " WHERE ownerid=" + str(userId) + \
                    " ORDER BY random() "
            planets = dbRows(query)
            
            for planet in planets:
                if planet_limit == 0 or nb_planet < planet_limit:

                    query = "INSERT INTO spy_planet(spy_id,  planet_id,  planet_name,  floor,  space, pct_ore, pct_hydrocarbon, ground) " + \
                            " VALUES(" + str(reportId) +"," + str(planet['id']) +"," + dosql(planet['name']) +"," + str(planet['floor']) + "," + str(planet['space']) + "," + str(planet['pct_ore']) + "," + str(planet['pct_hydrocarbon']) + "," + str(planet['ground']) + ")"
                    dbQuery(query)

                    nb_planet = nb_planet + 1

            #---
            
            if level >= 2:
            
                query = " SELECT researchid, level " + \
                        " FROM sp_list_researches(" + str(userId) + ") " + \
                        " WHERE level > 0" + \
                        " ORDER BY researchid "
                researches = dbRows(query)

                for research in researches:

                    query = "INSERT INTO spy_research(spy_id, research_id, research_level)" + \
                            " VALUES(" + str(reportId) +", " + str(research['researchid']) +", " + str(research['level']) +") "
                    dbQuery(query)
                    
            #---
            
            query = " INSERT INTO reports(ownerid, type, subtype, datetime, spyid, description)" + \
                    " VALUES(" + str(self.userId) + ", 8, 10, now() + " + str(spyingTime + nb_planet) + "*interval '1 minute', " + str(reportId) + ", sp_get_user(" + str(userId) + "))"
            dbQuery(query)
        
            #---
            
            spotted = random() < spottedChance
            if spotted:

                query = " UPDATE spy " + \
                        " SET spotted=" + str(spotted) + \
                        " WHERE id=" + str(reportId) + " AND userid=" + str(self.userId)
                dbQuery(query)

                query = " INSERT INTO reports(ownerid, type, subtype, datetime, spyid, description) " + \
                        " VALUES(" + str(userId) + ", 8, 1, now() + " + str(spyingTime + nb_planet) + "*interval '40 seconds', " + str(reportId) + ", sp_get_user(" + str(self.userId) + "))"
                dbQuery(query)
                
            #---
            
            query = "UPDATE users SET prestige_points=prestige_points - " + str(cost) + " WHERE id=" + str(self.userId)
            dbQuery(query)
            
        #---
        
        elif action == "planet":
            
            #---
            
            level = ToInt(request.POST.get("level"), -1)
            spotted = False
            category = 8
            
            #---
            
            g = ToInt(request.POST.get("g"), 0)
            s = ToInt(request.POST.get("s"), 0)
            p = ToInt(request.POST.get("p"), 0)
            
            userId = dbExecute("SELECT ownerid FROM nav_planet WHERE galaxy=" + str(g) + " AND sector=" + str(s) + " AND planet=" + str(p))
            if userId == None:
            
                messages.error(request, 'planet_not_exists')
                return HttpResponseRedirect(request.build_absolute_uri())
                
            elif userId == self.userId:
            
                messages.error(request, 'own_nation_planet')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            #---
            
            reportId = dbExecute("SELECT sp_create_spy('" + str(self.userId) + "', int2(" + str(3) + "), int2(" + str(level) + ") )")
            if reportId < 0:
                messages.error(request, 'general_error')
                return HttpResponseRedirect(request.build_absolute_uri())
                
            #---
            
            if level == 0:
            
                spottedChance = 0.6
                getinfoModifier = 0.05
                cost = self.planet_cost_lvl_0
                spyingTime = 5
                
            elif level == 1:
            
                spottedChance = 0.3
                getinfoModifier = 0.025
                cost = self.planet_cost_lvl_1
                spyingTime = 10
                
            elif level == 2:
            
                spottedChance = 0.15
                getinfoModifier = 0
                cost = self.planet_cost_lvl_2
                spyingTime = round(20 + random() * 10)
                
            elif level == 3:
            
                spottedChance = 0
                getinfoModifier = 0
                cost = self.planet_cost_lvl_3
                spyingTime = round(100 + random() * 50)

            #---
            
            if self.profile["prestige_points"] < cost:
                messages.error(request, 'not_enough_money')
                return HttpResponseRedirect(request.build_absolute_uri())
        
            #---
            
            query = " SELECT id, name, ownerid, sp_get_user(ownerid) AS owner_name, floor, space, floor_occupied, space_occupied,  " + \
                        " COALESCE((SELECT SUM(quantity*signature) " + \
                        " FROM planet_ships " + \
                        " LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id) " + \
                        " WHERE planet_ships.planetid=vw_planets.id),0) AS ground, " + \
                    " ore, hydrocarbon, ore_capacity, hydrocarbon_capacity, ore_production, hydrocarbon_production, " + \
                    " energy_consumption, energy_production, " + \
                    " radar_strength, radar_jamming, colonization_datetime, orbit_ore, orbit_hydrocarbon, " + \
                    " workers, workers_capacity, scientists, scientists_capacity, soldiers, soldiers_capacity, " + \
                    " pct_ore, pct_hydrocarbon" + \
                    " FROM vw_planets " + \
                    " WHERE galaxy=" + str(g) + " AND sector=" + str(s) + " AND planet=" + str(p)
            planet = dbRow(query)
            
            if planet['ownerid']:
                
                #---
                
                dbQuery("UPDATE spy SET target_name=sp_get_user(" + str(planet['ownerid']) + ") WHERE id=" + str(reportId))
                
                #---
                
                query = "INSERT INTO spy_planet(spy_id, planet_id, planet_name, owner_name, floor, space, pct_ore, pct_hydrocarbon, ground)" + \
                        " VALUES (" + str(reportId) +", " + str(planet['id']) + "," + dosql(planet['name']) +"," + dosql(planet['owner_name']) +"," + str(planet['floor']) + "," + str(planet['space']) + "," + str(planet['pct_ore']) + "," + str(planet['pct_hydrocarbon']) + "," + str(planet['ground']) + ")"
                dbQuery(query)
                
                #---
                
                query = " UPDATE spy_planet SET" + \
                        " radar_strength=" + str(planet['radar_strength']) + ", radar_jamming=" + str(planet['radar_jamming']) + ", " + \
                        " orbit_ore=" + str(planet['orbit_ore']) + ", orbit_hydrocarbon=" + str(planet['orbit_hydrocarbon']) + \
                        " WHERE spy_id=" + str(reportId) + " AND planet_id=" + str(planet['id'])
                dbQuery(query)
                
                #---
                
                query = "SELECT planetid, id, quantity, construction_maximum" + \
                        " FROM vw_buildings" + \
                        " WHERE planetid=" + str(planet['id']) + " AND quantity != 0 AND build_status IS NULL AND destruction_time IS NULL"
                rows = dbRows(query)
                
                i = 0
                for row in rows:

                    rand1 = random()

                    qty = row['quantity']

                    if rand1 < (getinfoModifier * i) and row['construction_maximum'] != 1:

                        rndmax = int(row['quantity'] * 1.5)
                        if rndmax <= row['quantity']: rndmax = rndmax + 1
                        rndmax = min(rndmax, row['construction_maximum'])
                        rndmin = int(row['quantity'] * 0.5)
                        if rndmin < 1: rndmin = 1
                        qty = int((rndmax - rndmin + 1) * random() + rndmin)

                    query = " INSERT INTO spy_building(spy_id, planet_id, building_id, quantity) " + \
                            " VALUES(" + str(reportId) + ", " + str(planet['id']) + ", " + str(row['id']) + ", " + str(qty) + " )"
                    dbQuery(query)
                    
                    i += 1

                #---
                    
                if level >= 1:
                
                    query = "UPDATE spy_planet SET" + \
                            " ore=" + str(planet['ore']) + ", hydrocarbon=" + str(planet['hydrocarbon']) + \
                            ", ore_capacity=" + str(planet['ore_capacity']) + ", hydrocarbon_capacity=" + str(planet['hydrocarbon_capacity']) + \
                            ", ore_production=" + str(planet['ore_production']) + ", hydrocarbon_production=" + str(planet['hydrocarbon_production']) + \
                            ", energy_consumption=" + str(planet['energy_consumption']) + ", energy_production=" + str(planet['energy_production']) + \
                            " WHERE spy_id=" + str(reportId) + " AND planet_id=" + str(planet['id'])
                    dbQuery(query)

                #---
                
                if level >= 2:

                    query = "UPDATE spy_planet SET" + \
                            " workers=" + str(planet['workers']) + ", workers_capacity=" + str(planet['workers_capacity']) + ", " + \
                            " scientists=" + str(planet['scientists']) + ", scientists_capacity=" + str(planet['scientists_capacity']) + ", " + \
                            " soldiers=" + str(planet['soldiers']) + ", soldiers_capacity=" + str(planet['soldiers_capacity']) + \
                            " WHERE spy_id=" + str(reportId) + " AND planet_id=" + str(planet['id'])
                    dbQuery(query)

                    query = "SELECT planetid, id, build_status, quantity, construction_maximum " + \
                            " FROM vw_buildings AS b " + \
                            " WHERE planetid=" + str(planet['id']) + " AND build_status IS NOT NULL"
                    rows = dbRows(query)
                    
                    i = 0
                    for row in rows:
                        
                        rand1 = random()

                        qty = row['quantity']

                        if rand1 < (getinfoModifier * i) and row['construction_maximum'] != 1:

                            rndmax = int(row['quantity'] * 1.5)
                            if rndmax <= row['quantity']: rndmax = rndmax + 1
                            rndmax = min(rndmax, row['construction_maximum'])
                            rndmin = int(row['quantity'] * 0.5)
                            if rndmin < 1: rndmin = 1
                            qty = int((rndmax - rndmin + 1) * random() + rndmin)

                        query = "INSERT INTO spy_building(spy_id, planet_id, building_id, endtime, quantity) " + \
                                " VALUES (" + str(reportId) + ", " + str(planet['id']) + ", " + str(row['id']) + ", now() + " + str(row['build_status']) + "* interval '1 second', " + str(qty) + " )"
                        dbQuery(query)
                        
                        i += 1
                
            else:
            
                query = " INSERT INTO spy_planet(spy_id, planet_id, floor, space) " + \
                        " VALUES(" + str(reportId) +", " + str(planet['id']) +", " + str(planet['floor']) +", " + str(planet['space']) +") "
                dbQuery(query)
                
                return HttpResponseRedirect(request.build_absolute_uri())
                
            #---
        
            query = " INSERT INTO reports(ownerid, type, subtype, datetime, spyid, planetid) " + \
                    " VALUES(" + str(self.userId) + ", 8, 30, now() + " + str(spyingTime) + "*interval '1 minute', " + str(reportId) + ", " + str(planet['id']) + ") "
            dbQuery(query)
        
            #---
            
            spotted = random() < spottedChance
            if spotted:

                query = " UPDATE spy " + \
                        " SET spotted=" + str(spotted) + \
                        " WHERE id=" + str(reportId) + " AND userid=" + str(self.userId)
                dbQuery(query)
                
                query = " INSERT INTO reports(ownerid, type, subtype, datetime, spyid, planetid, description) " + \
                        " VALUES(" + str(userId) + ", 8, 3, now() + " + str(spyingTime) + "*interval '40 seconds'," + str(reportId) + "," + str(planet['id']) + ", sp_get_user(" + str(self.userId) + "))"
                dbQuery(query)
                
            #---
            
            query = "UPDATE users SET prestige_points=prestige_points - " + str(cost) + " WHERE id=" + str(self.userId)
            dbQuery(query)
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    def get(self, request, *args, **kwargs):
    
        #---
        
        content = getTemplate(request, "s03/mercenary-intelligence")

        self.selectedMenu = "intelligence"
        
        #---

        content.setValue("nation_cost_lvl_0", self.nation_cost_lvl_0)
        content.setValue("nation_cost_lvl_1", self.nation_cost_lvl_1)
        content.setValue("nation_cost_lvl_2", self.nation_cost_lvl_2)
        content.setValue("nation_cost_lvl_3", self.nation_cost_lvl_3)

        content.setValue("planet_cost_lvl_0", self.planet_cost_lvl_0)
        content.setValue("planet_cost_lvl_1", self.planet_cost_lvl_1)
        content.setValue("planet_cost_lvl_2", self.planet_cost_lvl_2)
        content.setValue("planet_cost_lvl_3", self.planet_cost_lvl_3)
        
        #---

        return self.display(content, request)
