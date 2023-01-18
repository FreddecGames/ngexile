from .base import *

class View(BaseView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- get
        
        content = getTemplateContext(request, 'empire-view')
        
        self.selectedMenu = 'empire'
        
        # alliance data
        
        if self.profile['alliance_id']:
        
            query = 'SELECT announce, tag, name, defcon FROM alliances WHERE id=' + str(self.profile['alliance_id'])
            alliance = dbRow(query)
            content.assignValue('alliance', alliance)
        
        # stats data
        
        query = 'SELECT orientation, score, previous_score, mod_planets::integer, mod_commanders::integer FROM users WHERE id=' + str(self.profile['id'])
        stats = dbRow(query)
        
        stats['score_delta'] = stats['score'] - stats['previous_score']
        
        query = 'SELECT int4(count(1)) AS commanders FROM commanders WHERE recruited IS NOT NULL AND ownerid=' + str(self.profile['id'])
        result = dbRow(query)
        stats = stats | result
        
        query = 'SELECT int4(count(1)) AS players, (SELECT int4(count(1)) FROM vw_players WHERE score >= ' + str(stats['score']) + ') AS ranking FROM vw_players'
        result = dbRow(query)
        stats = stats | result
        
        query = 'SELECT count(1) AS planets,' + \
                ' sum(ore_production) AS ore_prod, sum(hydrocarbon_production) AS hydro_prod,' + \
                ' int4(sum(workers)) AS workers, int4(sum(scientists)) AS scientists, int4(sum(soldiers)) AS soldiers' + \
                ' FROM vw_planets WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.profile['id'])
        result = dbRow(query)
        stats = stats | result
        
        query = 'SELECT int4(sum(cargo_workers)) AS workers, int4(sum(cargo_scientists)) AS scientists, int4(sum(cargo_soldiers)) AS soldiers' + \
                ' FROM fleets WHERE ownerid=' + str(self.profile['id'])
        result = dbRow(query)
        stats['workers'] += result['workers']
        stats['scientists'] += result['scientists']
        stats['soldiers'] += result['soldiers']
        
        content.assignValue('stats', stats)
        
        # movings data
        
        query = 'SELECT fleets.id, fleets.name, fleets.owner_name, fleets.signature, fleets.attackonsight AS stance,' + \
                ' COALESCE(((SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = fleets.ownerid)), -3) AS relation,' + \
                ' fleets.planetid, fleets.planet_name, COALESCE(((SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = fleets.planet_ownerid)), -3) AS planet_relation, fleets.planet_galaxy, fleets.planet_sector, fleets.planet_planet,' + \
                ' fleets.destplanetid, fleets.destplanet_name, COALESCE(((SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = fleets.destplanet_ownerid)), -3) AS destplanet_relation, fleets.destplanet_galaxy, fleets.destplanet_sector, fleets.destplanet_planet,' + \
                ' COALESCE(fleets.remaining_time, 0) AS remaining_time,' + \
                ' (SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = fleets.planet_galaxy AND nav_planet.sector = fleets.planet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = users.id)) AS from_radarstrength' + \
                ' FROM users, vw_fleets AS fleets ' + \
                ' WHERE users.id=' + str(self.profile['id']) + ' AND (action = 1 OR action = -1) AND (ownerid=' + str(self.profile['id']) + ' OR (destplanetid IS NOT NULL AND destplanetid IN (SELECT id FROM nav_planet WHERE ownerid=' + str(self.profile['id']) + ')))' + \
                ' ORDER BY COALESCE(remaining_time, 0), ownerid'
        results = dbRows(query)
        movings = results
        
        for item in movings:
            if item['planetid']:
                if item['from_radarstrength'] > 0 or item['relation'] >= 0:
                    item['from'] = True            
        
        content.assignValue('movings', movings)
        
        '''

        #
        # view current buildings constructions
        #
        query = "SELECT p.id, p.name, p.galaxy, p.sector, p.planet, b.buildingid, b.remaining_time, destroying" +\
                " FROM nav_planet AS p" +\
                "	 LEFT JOIN vw_buildings_under_construction2 AS b ON (p.id=b.planetid)"+\
                " WHERE p.ownerid="+str(self.profile['id'])+\
                " ORDER BY p.id, destroying, remaining_time"
        oRs = oConnExecuteAll(query)

        lastplanet = -1

        constructionyards = []
        items = 0
        for item in oRs:
            if item[0] != lastplanet:
                planet = {"buildings":[]}
                lastplanet = item[0]
                items = 0

                planet["planetid"] = item[0]
                planet["planetname"] = item[1]
                planet["galaxy"] = item[2]
                planet["sector"] = item[3]
                planet["planet"] = item[4]
                constructionyards.append(planet)

            if item[5]:
                building = {}
                building["buildingid"] = item[5]
                building["building"] = getBuildingLabel(item[5])
                building["time"] = item[6]

                if item[7]:
                    building["destroy"] = True
                    
                planet["buildings"].append(building)

                items = items + 1

        content.assignValue("constructionyards", constructionyards)

        #
        # view current ships constructions
        #
        query = "SELECT p.id, p.name, p.galaxy, p.sector, p.planet, s.shipid, s.remaining_time, s.recycle, p.shipyard_next_continue IS NOT NULL, p.shipyard_suspended," +\
                " (SELECT shipid FROM planet_ships_pending WHERE planetid=p.id ORDER BY start_time LIMIT 1)" +\
                " FROM nav_planet AS p" +\
                "	LEFT JOIN vw_ships_under_construction AS s ON (p.id=s.planetid AND p.ownerid=s.ownerid AND s.end_time IS NOT NULL)"+\
                " WHERE (s.recycle OR EXISTS(SELECT 1 FROM planet_buildings WHERE (buildingid = 105 OR buildingid = 205) AND planetid=p.id)) AND p.ownerid=" + str(self.profile['id']) +\
                " ORDER BY p.id, s.remaining_time"
        oRs = oConnExecuteAll(query)

        if oRs:
            lastplanet=0

            shipyards = []
            items = 0
            for item in oRs:
                if item[0] != lastplanet:
                    planet = {}
                    shipyards.append(planet)
                    lastplanet = item[0]

                planet["planetid"] = item[0]
                planet["planetname"] = item[1]
                planet["galaxy"] = item[2]
                planet["sector"] = item[3]
                planet["planet"] = item[4]
                planet["shipid"] = item[5]
                planet["shiplabel"] = getShipLabel(item[5])
                planet["time"] = item[6]
    
                if item[10]:
                    planet["waiting_ship"] = getShipLabel(item[10])

                if item[5]:
                    if item[7]: planet["recycle"] = True
                    planet["ship"] = True
                    items = items + 1
                elif item[9]:
                    planet["suspended"] = True
                    items = items + 1
                elif item[8]:
                    planet["waiting_resources"] = True
                    items = items + 1
                else:
                    planet["none"] = True

            content.assignValue("shipyards", shipyards)

        #
        # view current research
        #
        query = "SELECT researchid, int4(date_part('epoch', end_time-now()))" +\
                " FROM researches_pending" +\
                " WHERE userid=" + str(self.profile['id'])
        oRs = oConnExecuteAll(query)

        i = 0
        if oRs:
            for item in oRs:
                content.assignValue("researchid", item[0])
                content.assignValue("researchlabel", getResearchLabel(item[0]))
                content.assignValue("researchtime", item[1])
                content.parse("research")
                i = i + 1

        if i==0: content.parse("noresearch")

        query =	"SELECT f.id, f.name, f.signature, f.ownerid, " +\
                "COALESCE((( SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = f.ownerid)), -3) AS owner_relation, f.owner_name," +\
                "f.planetid, f.planet_name, COALESCE((( SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = f.planet_ownerid)), -3) AS planet_owner_relation, f.planet_galaxy, f.planet_sector, f.planet_planet, " +\
                "f.destplanetid, f.destplanet_name, COALESCE((( SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = f.destplanet_ownerid)), -3) AS destplanet_owner_relation, f.destplanet_galaxy, f.destplanet_sector, f.destplanet_planet, " +\
                "f.planet_owner_name, f.destplanet_owner_name, f.speed," +\
                "COALESCE(f.remaining_time, 0), COALESCE(f.total_time-f.remaining_time, 0), " +\
                "( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.planet_galaxy AND nav_planet.sector = f.planet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = users.id)) AS from_radarstrength, " +\
                "( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.destplanet_galaxy AND nav_planet.sector = f.destplanet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = users.id)) AS to_radarstrength, " +\
                "attackonsight" +\
                " FROM users, vw_fleets f " +\
                " WHERE users.id="+str(self.profile['id'])+" AND (""action"" = 1 OR ""action"" = -1) AND (ownerid="+str(self.profile['id'])+" OR (destplanetid IS NOT NULL AND destplanetid IN (SELECT id FROM nav_planet WHERE ownerid="+str(self.profile['id'])+")))" +\
                " ORDER BY ownerid, COALESCE(remaining_time, 0)"
        oRs = oConnExecuteAll(query)

        fleets = []
        i = 0
        if oRs:
            for item in oRs:
    
                parseFleet = True
                fleet = {}
    
                fleet["signature"] = item[2]
    
                # display planet names f (from) and t (to)
    
                fleet["f_planetname"] = getPlanetName(item[8], item[23], item[18], item[7])
                fleet["f_planetid"] = item[6]
                fleet["f_g"] = item[9]
                fleet["f_s"] = item[10]
                fleet["f_p"] = item[11]
                fleet["f_relation"] = item[8]
    
                fleet["t_planetname"] = getPlanetName(item[14], item[24], item[19], item[13])
                fleet["t_planetid"] = item[12]
                fleet["t_g"] = item[15]
                fleet["t_s"] = item[16]
                fleet["t_p"] = item[17]
                fleet["t_relation"] = item[14]
    
                fleet["time"] = item[21]
                
                # retrieve the radar strength where the fleet comes from
                extRadarStrength = item[23]
                
                # retrieve the radar strength where the fleet goes to
                incRadarStrength = item[24]
    
                # if remaining time is longer than our radar range
                if item[6]: # if origin planet is not null
    
                    if item[4] < rAlliance and (item[21] > sqrt(incRadarStrength)*6*1000/item[20]*3600) and (extRadarStrength == 0 or incRadarStrength == 0):
                        parseFleet = False
                    else:
                        # display origin if we have a radar or the planet owner is an ally or the fleet is in NAP
                        if extRadarStrength > 0 or item[4] >= rAlliance or item[8] >= rFriend:
                            fleet["movingfrom"] = True
                        else:
                            fleet["no_from"] = True
    
                if parseFleet:
    
                    # assign either fleet name or fleet owner name
                    if item[4] == rSelf:
                        # Assign fleet (id & name)
                        fleet["id"] = item[0]
                        fleet["name"] = item[1]
                        if item[25]:
                            fleet["attack"] = True
                        else:
                            fleet["defend"] = True
                        fleet["owned"] = True
                    elif item[4] == rAlliance:
                        # assign fleet owner (id & name)
                        fleet["id"] = item[3]
                        fleet["name"] = item[5]
                        if item[25]:
                            fleet["attack"] = True
                        else:
                            fleet["defend"] = True
                        fleet["ally"] = True
                    elif item[4] == rFriend:
                        # assign fleet owner (id & name)
                        fleet["id"] = item[3]
                        fleet["name"] = item[5]
                        if item[25]:
                            fleet["attack"] = True
                        else:
                            fleet["defend"] = True
                        fleet["friend"] = True
                    else:
                        # assign fleet owner (id & name)
                        fleet["id"] = item[3]
                        fleet["name"] = item[5]
                        fleet["hostile"] = True
    
                    fleets.append(fleet)
                    i = i + 1

        if i==0: content.parse("nofleets")
        content.assignValue("fleets", fleets)
        
        # upkeep
        
        hours = 24 - timezone.now().hour

        query = "SELECT scientists,soldiers,planets,ships_signature,ships_in_position_signature,ships_parked_signature," + \
                " cost_planets2,cost_scientists,cost_soldiers,cost_ships,cost_ships_in_position,cost_ships_parked," + \
                " int4(upkeep_scientists + scientists*cost_scientists/24*"+str(hours)+"),"+ \
                " int4(upkeep_soldiers + soldiers*cost_soldiers/24*"+str(hours)+"),"+ \
                " int4(upkeep_planets + cost_planets2/24*"+str(hours)+"),"+ \
                " int4(upkeep_ships + ships_signature*cost_ships/24*"+str(hours)+"),"+ \
                " int4(upkeep_ships_in_position + ships_in_position_signature*cost_ships_in_position/24*"+str(hours)+"),"+ \
                " int4(upkeep_ships_parked + ships_parked_signature*cost_ships_parked/24*"+str(hours)+"),"+ \
                " commanders, commanders_salary, cost_commanders, upkeep_commanders + int4(commanders_salary*cost_commanders/24*"+str(hours)+")" + \
                " FROM vw_players_upkeep" + \
                " WHERE userid=" + str(self.profile['id'])
        oRs = oConnExecute(query)

        content.assignValue("commanders_estimated_cost", int(oRs[21]))
        content.assignValue("scientists_estimated_cost", oRs[12])
        content.assignValue("soldiers_estimated_cost", oRs[13])
        content.assignValue("planets_estimated_cost", oRs[14])
        content.assignValue("ships_estimated_cost", oRs[15])
        content.assignValue("ships_in_position_estimated_cost", oRs[16])
        content.assignValue("ships_parked_estimated_cost", oRs[17])

        content.assignValue("total_estimation", int(oRs[12] + oRs[13] + oRs[14] + oRs[15] + oRs[16] + oRs[17] + oRs[21]))
        '''
        return self.display(content)
