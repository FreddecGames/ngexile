# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################    
    
    def get(self, request, format=None):
        
        tpl = getTemplate()
        
        #---

        if self.allianceId:
        
            query = 'SELECT announce, tag, name, defcon FROM alliances WHERE id=' + str(self.allianceId)
            alliance = dbRow(query)
            tpl.set('alliance', alliance)

            if self.allianceRights: tpl.set('alliance_rank_label', self.allianceRights['label'])

        #---
        
        tpl.set('orientation', self.profile['orientation'])
        tpl.set('nation', self.profile['username'])
        tpl.set('stat_score', self.profile['score'])
        tpl.set('stat_score_delta', self.profile['score'] - self.profile['previous_score'])
        tpl.set('stat_credits', self.profile['credits'])
        tpl.set('stat_victory_marks', self.profile['prestige_points'])
        tpl.set('stat_maxcolonies', int(self.profile['mod_planets']))

        #---

        query = 'SELECT int4(count(1)) AS stat_players, (SELECT int4(count(1)) FROM vw_players WHERE score >= ' + str(self.profile['score']) + ') AS stat_rank FROM vw_players'
        row = dbRow(query)
                
        tpl.set('stat_rank', row['stat_rank'])
        tpl.set('stat_players', row['stat_players'])

        #---

        query = 'SELECT (SELECT score_prestige AS stat_score_battle FROM users WHERE id=' + str(self.userId) + '), (SELECT int4(count(1)) AS stat_rank_battle FROM vw_players WHERE score_prestige >= (SELECT score_prestige FROM users WHERE id=' + str(self.userId) + '))'
        row = dbRow(query)

        tpl.set('stat_score_battle', row['stat_score_battle'])
        tpl.set('stat_rank_battle', row['stat_rank_battle'])

        #---
        
        query = 'SELECT count(1) AS stat_colonies, sum(ore_production) AS stat_prod_ore, sum(hydrocarbon_production) AS stat_prod_hydrocarbon, ' + \
                ' int4(sum(workers)) AS workers, int4(sum(scientists)) AS scientists, int4(sum(soldiers)) AS soldiers, now() AS date' + \
                ' FROM vw_planets WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=' + str(self.userId)
        row = dbRow(query)

        tpl.set('date', row['date'])
        tpl.set('stat_colonies', row['stat_colonies'])
        tpl.set('stat_prod_ore', row['stat_prod_ore'])
        tpl.set('stat_prod_hydrocarbon', row['stat_prod_hydrocarbon'])
        
        #---

        row2 = dbRow('SELECT COALESCE(int4(sum(cargo_workers)), 0) AS workers, COALESCE(int4(sum(cargo_scientists)), 0) AS scientists, COALESCE(int4(sum(cargo_soldiers)), 0) AS soldiers FROM fleets WHERE ownerid=' + str(self.userId))

        tpl.set('stat_workers', row['workers'] + row2['workers'])
        tpl.set('stat_scientists', row['scientists'] + row2['scientists'])
        tpl.set('stat_soldiers', row['soldiers'] + row2['soldiers'])

        #---

        query =	'SELECT f.id, f.name, f.signature, f.ownerid,' + \
                'COALESCE((( SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = f.ownerid)), -3) AS owner_relation, f.owner_name,' + \
                'f.planetid, f.planet_name, COALESCE((( SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = f.planet_ownerid)), -3) AS planet_owner_relation, f.planet_galaxy, f.planet_sector, f.planet_planet,' + \
                'f.destplanetid, f.destplanet_name, COALESCE((( SELECT vw_relations.relation FROM vw_relations WHERE vw_relations.user1 = users.id AND vw_relations.user2 = f.destplanet_ownerid)), -3) AS destplanet_owner_relation, f.destplanet_galaxy, f.destplanet_sector, f.destplanet_planet,' + \
                'f.planet_owner_name, f.destplanet_owner_name, f.speed,' + \
                'COALESCE(f.remaining_time, 0) AS time, COALESCE(f.total_time-f.remaining_time, 0),' + \
                '( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.planet_galaxy AND nav_planet.sector = f.planet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = users.id)) AS from_radarstrength,' + \
                '( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.destplanet_galaxy AND nav_planet.sector = f.destplanet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = users.id)) AS to_radarstrength,' + \
                'attackonsight' + \
                ' FROM users, vw_fleets f ' + \
                ' WHERE users.id=' + str(self.userId) + ' AND (action = 1 OR action = -1) AND (ownerid=' + str(self.userId) + ' OR (destplanetid IS NOT NULL AND destplanetid IN (SELECT id FROM nav_planet WHERE ownerid=' + str(self.userId) + ')))' + \
                ' ORDER BY COALESCE(remaining_time, 0), ownerid'
        rows = dbRows(query)
        
        fleets = []
        tpl.set('fleets', fleets)

        for row in rows:

            extRadarStrength = row['from_radarstrength']
            incRadarStrength = row['to_radarstrength']
            
            if row['owner_relation'] < rAlliance and (row['time'] > math.sqrt(incRadarStrength) * 6 * 1000 / row['speed'] * 3600) and (extRadarStrength == 0 or incRadarStrength == 0):
                continue
            else:
                    
                fleet = {}
                fleets.append(fleet)

                fleet['id'] = row['id']
                fleet['name'] = row['name']
                fleet['time'] = row['time']
                fleet['signature'] = row['signature']
                fleet['attackonsight'] = row['attackonsight']
                
                fleet['owner_name'] = row['owner_name']
                fleet['owner_relation'] = row['owner_relation']

                fleet['t_planetname'] = self.getPlanetName(row['destplanet_owner_relation'], row['to_radarstrength'], row['destplanet_owner_name'], row['destplanet_name'])
                fleet['t_planetid'] = row['destplanetid']
                fleet['t_g'] = row['destplanet_galaxy']
                fleet['t_s'] = row['destplanet_sector']
                fleet['t_p'] = row['destplanet_planet']
                fleet['t_relation'] = row['destplanet_owner_relation']

                if extRadarStrength > 0 or row['owner_relation'] >= rAlliance or row['planet_owner_relation'] >= rFriend:
                
                    fleet['f_planetname'] = self.getPlanetName(row['planet_owner_relation'], row['from_radarstrength'], row['planet_owner_name'], row['planet_name'])
                    fleet['f_planetid'] = row['planetid']
                    fleet['f_g'] = row['planet_galaxy']
                    fleet['f_s'] = row['planet_sector']
                    fleet['f_p'] = row['planet_planet']
                    fleet['f_relation'] = row['planet_owner_relation']


        #---
        
        query = 'SELECT researchid, int4(date_part(\'epoch\', end_time-now())) AS time, label' + \
                ' FROM researches_pending' + \
                '    LEFT JOIN db_research ON (researchid = db_research.id)' + \
                ' WHERE userid=' + str(self.userId) + ' LIMIT 1'
        row = dbRow(query)
        tpl.set('research', row)

        #---
        
        query = 'SELECT p.id, p.name, p.galaxy, p.sector, p.planet, b.buildingid, b.remaining_time, destroying, label' + \
                ' FROM nav_planet AS p' + \
                '	 LEFT JOIN vw_buildings_under_construction2 AS b ON (p.id=b.planetid)' + \
                '    LEFT JOIN db_buildings ON (b.buildingid = db_buildings.id)' + \
                ' WHERE p.ownerid=' + str(self.userId)+\
                ' ORDER BY p.id, destroying, remaining_time DESC'
        rows = dbRows(query)

        constructionyards = []
        tpl.set('constructionyards', constructionyards)
        
        lastplanet = -1

        for row in rows:
        
            if row['id'] != lastplanet:
            
                planet = { 'buildings':[] }
                constructionyards.append(planet)
                
                lastplanet = row['id']

                planet['planetid'] = row['id']
                planet['planetname'] = row['name']
                planet['galaxy'] = row['galaxy']
                planet['sector'] = row['sector']
                planet['planet'] = row['planet']

            if row['buildingid']:
            
                building = {}
                building['buildingid'] = row['buildingid']
                building['building'] = row['label']
                building['time'] = row['remaining_time']
                building['destroying'] = row['destroying']
                    
                planet['buildings'].append(building)

        #---
        
        query = 'SELECT p.id, p.name, p.galaxy, p.sector, p.planet, s.shipid, s.remaining_time, s.recycle, (p.shipyard_next_continue IS NOT NULL) AS waiting_resources, label,' + \
                ' (SELECT label FROM planet_ships_pending LEFT JOIN db_ships ON (planet_ships_pending.shipid = db_ships.id) WHERE planetid=p.id ORDER BY start_time LIMIT 1) AS waiting_label' + \
                ' FROM nav_planet AS p' + \
                '	LEFT JOIN vw_ships_under_construction AS s ON (p.id=s.planetid AND p.ownerid=s.ownerid AND s.end_time IS NOT NULL)' + \
                '   LEFT JOIN db_ships ON (s.shipid = db_ships.id)' + \
                ' WHERE (s.recycle OR EXISTS(SELECT 1 FROM planet_buildings WHERE (buildingid = 105 OR buildingid = 205) AND planetid=p.id)) AND p.ownerid=' + str(self.userId) +\
                ' ORDER BY p.id, s.remaining_time DESC'
        rows = dbRows(query)

        if rows:
        
            lastplanet = -1

            shipyards = []
            tpl.set('shipyards', shipyards)
        
            for row in rows:
            
                if row['id'] != lastplanet:
                
                    planet = {}
                    shipyards.append(planet)
                    
                    lastplanet = row['id']

                planet['planetid'] = row['id']
                planet['planetname'] = row['name']
                planet['galaxy'] = row['galaxy']
                planet['sector'] = row['sector']
                planet['planet'] = row['planet']                
                planet['shipid'] = row['shipid']
                planet['shiplabel'] = row['label']
                planet['waiting_label'] = row['waiting_label']
                planet['time'] = row['remaining_time']
                planet['recycle'] = row['recycle']
                planet['waiting_resources'] = row['waiting_resources']
                
        #---
        
        return Response(tpl.data)
