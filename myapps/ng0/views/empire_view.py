# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GetView):
    
    tab_selected = 'view'
    menu_selected = 'empire'
    
    template_name = 'empire_view'
    
    def display(self, request):
        
        #---

        query =	'SELECT f.id, f.name, f.signature, f.remaining_time,' + \
                ' f.ownerid, COALESCE(((SELECT r.relation FROM vw_relations r WHERE r.user1 = u.id AND r.user2 = f.ownerid)), -3) AS owner_relation, f.owner_name,' + \
                ' f.planetid, COALESCE(((SELECT r.relation FROM vw_relations r WHERE r.user1 = u.id AND r.user2 = f.planet_ownerid)), -3) AS planet_relation, f.planet_galaxy, f.planet_sector, f.planet_planet,' + \
                ' f.destplanetid, COALESCE(((SELECT r.relation FROM vw_relations r WHERE r.user1 = u.id AND r.user2 = f.destplanet_ownerid)), -3) AS destplanet_relation, f.destplanet_galaxy, f.destplanet_sector, f.destplanet_planet,' + \
                ' (SELECT int4(COALESCE(max(p.radar_strength), 0)) FROM nav_planet p WHERE p.galaxy = f.planet_galaxy AND p.sector = f.planet_sector AND p.ownerid IS NOT NULL AND EXISTS (SELECT 1 FROM vw_friends_radars rd WHERE rd.friend = p.ownerid AND rd.userid = u.id)) AS from_radarstrength,' + \
                ' (SELECT int4(COALESCE(max(p.radar_strength), 0)) FROM nav_planet p WHERE p.galaxy = f.destplanet_galaxy AND p.sector = f.destplanet_sector AND p.ownerid IS NOT NULL AND EXISTS (SELECT 1 FROM vw_friends_radars rd WHERE rd.friend = p.ownerid AND rd.userid = u.id)) AS to_radarstrength' + \
                ' FROM users u, vw_fleets f ' + \
                ' WHERE u.id=' + str(self.userId) + ' AND (f.action = 1 OR f.action = -1) AND (f.ownerid=' + str(self.userId) + ' OR (f.destplanetid IS NOT NULL AND f.destplanetid IN (SELECT p.id FROM nav_planet p WHERE p.ownerid=' + str(self.userId) + ')))' + \
                ' ORDER BY f.remaining_time, f.ownerid'
        rows = dbRows(query)
        
        fleets = []
        self.tpl.setValue('fleets', fleets)

        for row in rows:

            extRadarStrength = row['from_radarstrength']
            incRadarStrength = row['to_radarstrength']
            
            if row['owner_relation'] >= 1 or incRadarStrength > 0:
                
                fleets.append(row)

                if extRadarStrength <= 0 and row['owner_relation'] < 1 and row['planet_relation'] < 0:
                    fleet['planetid'] = None
        
        #---
        
        query = 'SELECT p.researchid AS id, db.label, int4(date_part(\'epoch\', p.end_time - now())) AS remaining_time' + \
                ' FROM researches_pending p' + \
                '  LEFT JOIN db_research db ON (researchid = db.id)' + \
                ' WHERE p.userid=' + str(self.userId) + ' LIMIT 1'
        row = dbRow(query)
        
        self.tpl.setValue('research', row)

        #---
        
        query = 'SELECT p.id, p.name, p.galaxy, p.sector, p.planet, b.buildingid, b.remaining_time, b.destroying, db.label' + \
                ' FROM nav_planet p' + \
                '  LEFT JOIN vw_buildings_under_construction2 b ON (p.id = b.planetid)' + \
                '  LEFT JOIN db_buildings db ON (b.buildingid = db.id)' + \
                ' WHERE p.ownerid=' + str(self.userId) + \
                ' ORDER BY p.id, b.destroying, b.remaining_time DESC'
        rows = dbRows(query)

        planet_buildings = []
        self.tpl.setValue('planet_buildings', planet_buildings)
        
        lastplanet = -1
        for row in rows:
        
            if row['id'] != lastplanet:
            
                planet = { 'buildings':[] }
                planet_buildings.append(planet)
                
                lastplanet = row['id']

                planet['id'] = row['id']
                planet['name'] = row['name']
                planet['galaxy'] = row['galaxy']
                planet['sector'] = row['sector']
                planet['planet'] = row['planet']
            
            if row['buildingid']:
            
                building = {}
                planet['buildings'].append(building)
                
                building['id'] = row['buildingid']
                building['name'] = row['label']
                building['destroying'] = row['destroying']
                building['remaining_time'] = row['remaining_time']
            
        #---
        
        query = 'SELECT p.id, p.name, p.galaxy, p.sector, p.planet, s.shipid, s.remaining_time, s.recycle, db.label, (p.shipyard_next_continue IS NOT NULL) AS waiting, ' + \
                ' (SELECT label FROM planet_ships_pending LEFT JOIN db_ships ON (planet_ships_pending.shipid = db_ships.id) WHERE planetid = p.id ORDER BY start_time LIMIT 1) AS waiting_label' + \
                ' FROM nav_planet p' + \
                '	LEFT JOIN vw_ships_under_construction s ON (p.id = s.planetid AND s.end_time IS NOT NULL)' + \
                '   LEFT JOIN db_ships db ON (s.shipid = db.id)' + \
                ' WHERE (EXISTS(SELECT 1 FROM planet_buildings WHERE (buildingid = 105 OR buildingid = 205) AND planetid = p.id)) AND p.ownerid=' + str(self.userId) + \
                ' ORDER BY p.id, s.remaining_time DESC'
        rows = dbRows(query)
        
        self.tpl.setValue('planet_ships', rows)
