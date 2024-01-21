# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):
    
    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
    
        self.selectedMenu = 'map'
        
        tpl = getTemplate(request, 'map')
        
        #---

        self.showHeader = True
        self.headerUrl = '/s03/map/'
        
        #---
        
        galaxy = request.GET.get('g', '')
        sector = request.GET.get('s', '')

        planet = request.GET.get('planet', '')
        if planet != '':
        
            galaxy = self.currentPlanetGalaxy
            sector = self.currentPlanetSector
            
        else:
        
            if galaxy != '': galaxy = ToInt(galaxy, self.currentPlanetGalaxy)
            if sector != '': sector = ToInt(sector, self.currentPlanetSector)

        tpl.set('galaxy', galaxy)
        tpl.set('sector', sector)

        #---
        
        if galaxy == '':

            #---
            
            query = 'SELECT n.id, ' + \
                    ' n.colonies > 0,' + \
                    ' False AND EXISTS(SELECT 1 FROM nav_planet WHERE galaxy=n.id AND ownerid IN (SELECT friend FROM vw_friends WHERE vw_friends.userid=' + str(self.userId) + ') LIMIT 1) AS hasfriend,' + \
                    ' EXISTS(SELECT 1 FROM nav_planet WHERE galaxy=n.id AND ownerid IN (SELECT ally FROM vw_allies WHERE vw_allies.userid=' + str(self.userId) + ') LIMIT 1) AS hasally,' + \
                    ' EXISTS(SELECT 1 FROM nav_planet WHERE galaxy=n.id AND ownerid = ' + str(self.userId) + ' LIMIT 1) AS hasplanet' + \
                    ' FROM nav_galaxies AS n' + \
                    ' ORDER BY n.id;'
            galaxies = dbRows(query)
            tpl.set('galaxies', galaxies)
                            
            #---
            
            return self.display(tpl, request)

        #---

        elif sector == '':

            #---
            
            query = 'SELECT sp_get_galaxy_planets(' + str(galaxy) + ',' + str(self.userId) + ')'
            mapgalaxy = dbExecute(query)
            if mapgalaxy == None: return HttpResponseRedirect('/s03/map')
            tpl.set('mapgalaxy', mapgalaxy)

            #---
            
            query = 'SELECT alliances.tag, round(100.0 * sum(n.score) / COALESCE((SELECT sum(score) FROM nav_planet WHERE galaxy=n.galaxy), 1)) AS percent' + \
                    ' FROM nav_planet AS n' + \
                    '    INNER JOIN users ON (users.id = n.ownerid)' + \
                    '    INNER JOIN alliances ON (users.alliance_id = alliances.id)' + \
                    ' WHERE galaxy=' + str(galaxy) + \
                    ' GROUP BY galaxy, alliances.tag' + \
                    ' ORDER BY sum(n.score) DESC LIMIT 3'
            sov = dbRows(query)
            tpl.set('sov', sov)

            #---

            query = 'SELECT date_part(\'epoch\', protected_until-now()) FROM nav_galaxies WHERE id=' + str(galaxy)
            result = dbExecute(query)
            tpl.set('protected_until', int(result))

            #---

            query = 'SELECT sell_ore, sell_hydrocarbon FROM sp_get_resource_price(' + str(self.userId) + ',' + str(galaxy) + ', false)'
            price = dbRow(query)
            tpl.set('price', price)
            
            #---

            return self.display(tpl, request)

        #---

        else:
        
            #---
        
            tpl.set('sector0', self.getSector(sector,-1,-1))
            tpl.set('sector1', self.getSector(sector, 0,-1))
            tpl.set('sector2', self.getSector(sector, 1,-1))
            tpl.set('sector3', self.getSector(sector, 1, 0))
            tpl.set('sector4', self.getSector(sector, 1, 1))
            tpl.set('sector5', self.getSector(sector, 0, 1))
            tpl.set('sector6', self.getSector(sector,-1, 1))
            tpl.set('sector7', self.getSector(sector,-1, 0))

            #---
            
            query = 'SELECT f.planetid, f.id, f.name, sp_relation(f.ownerid, ' + str(self.userId) + ') AS relation, f.signature,' + \
                    '    EXISTS(SELECT 1 FROM fleets AS fl WHERE fl.planetid=f.planetid and fl.action != 1 and fl.action != -1 and fl.ownerid IN (SELECT ally FROM vw_allies WHERE userid=' + str(self.userId) + ') LIMIT 1) AS allied,' + \
                    ' (action=1 OR action=-1) AS fleeing, (SELECT tag FROM alliances WHERE id=users.alliance_id) AS tag, username, shared,' + \
                    '    EXISTS(SELECT 1 FROM fleets AS fl WHERE fl.planetid=f.planetid and fl.action != 1 and fl.action != -1 and fl.ownerid =' + str(self.userId) + ' LIMIT 1) AS owned' + \
                    ' FROM fleets as f' + \
                    '    INNER JOIN users ON (f.ownerid=users.id)' + \
                    ' WHERE ((action != 1 AND action != -1) OR engaged) AND' + \
                    '    planetid >= sp_first_planet(' + str(galaxy) + ',' + str(sector) + ') AND planetid <= sp_last_planet(' + str(galaxy) + ',' + str(sector) + ')' + \
                    ' ORDER BY f.planetid, upper(f.name)'
            fleetsArray = dbRows(query)

            #---
            
            query = 'SELECT planetid, label, description' + \
                    ' FROM planet_buildings' + \
                    '    INNER JOIN db_buildings ON db_buildings.id=buildingid' + \
                    ' WHERE planetid >= sp_first_planet(' + str(galaxy) + ',' + str(sector) + ') AND planetid <= sp_last_planet(' + str(galaxy) + ',' + str(sector) + ') AND is_planet_element' + \
                    ' ORDER BY planetid, upper(label)'
            elementsArray = dbRows(query)

            #---

            query = 'SELECT * FROM sp_get_user_rs(' + str(self.userId) + ',' + str(galaxy) + ',' + str(sector) + ')'
            radarstrength = dbExecute(query)

            #---
            
            if self.allianceId == None: aid = -1
            else: aid = self.allianceId

            #---
            
            query = 'SELECT nav_planet.id, nav_planet.planet, nav_planet.name, nav_planet.ownerid,' + \
                    ' users.username, sp_relation(nav_planet.ownerid,' + str(self.userId) + ') AS relation, floor, space, GREATEST(0, radar_strength) AS radar_strength, radar_jamming,' + \
                    ' orbit_ore, orbit_hydrocarbon, alliances.tag,' + \
                    ' (SELECT SUM(quantity*signature) FROM planet_ships LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id) WHERE planet_ships.planetid=nav_planet.id) AS ground, ' + \
                    ' floor_occupied, planet_floor, production_frozen, warp_to IS NOT NULL OR vortex_strength > 0 AS vortex,' + \
                    ' planet_pct_ore, planet_pct_hydrocarbon, spawn_ore, spawn_hydrocarbon, vortex_strength,' + \
                    ' COALESCE(buy_ore, 0) AS buy_ore, COALESCE(buy_hydrocarbon, 0) as buy_hydrocarbon,' + \
                    ' sp_locs_shared(COALESCE(' + str(aid) + ', -1), COALESCE(users.alliance_id, -1)) AS locs_shared' + \
                    ' FROM nav_planet' + \
                    '    LEFT JOIN users ON (users.id = ownerid)' + \
                    '    LEFT JOIN alliances ON (users.alliance_id=alliances.id)' + \
                    ' WHERE galaxy=' + str(galaxy) + ' AND sector=' + str(sector) + \
                    ' ORDER BY planet'
            planets = dbRows(query)
            tpl.set('locations', planets)
            
            for planet in planets:
                
                #---
                
                rel = planet['relation']
                if rel == rAlliance and not self.hasRight('can_use_alliance_radars'): rel = rWar
                if rel == rFriend and not planet['locs_shared'] and planet['ownerid'] != 3: rel = rWar
                
                #---
                
                hasPlanetInfo = True
                
                displayElements = False
                displayResources = False
                displayPlanetInfo = False

                allyfleetcount = 0
                enemyfleetcount = 0
                friendfleetcount = 0
                
                #---
                
                planet['fleets'] = []
                for fleet in fleetsArray:
                    if fleet['planetid'] == planet['id']:
                        if (self.hasRight('can_use_alliance_radars') and (rel >= rAlliance or fleet['allied'])) or radarstrength > planet['radar_jamming'] or fleet['owned']:
    
                            planet['fleets'].append(fleet)
                            
                            fleet['fleetid'] = 0
                            
                            if fleet['tag'] == None: fleet['tag'] = ''
                            
                            if (planet['relation'] > rFriend) or (fleet['relation'] > rFriend) or (radarstrength > planet['radar_jamming']) or (fleet['allied'] and planet['radar_strength'] == 0): fleet['signature'] = fleet['signature']
                            else: fleet['signature'] = -1
    
                            if fleet['relation'] == rSelf:
                            
                                fleet['fleetid'] = fleet['id']
                                allyfleetcount = allyfleetcount + 1
                                friendfleetcount = friendfleetcount + 1
                                
                            elif fleet['relation'] == rAlliance:
                            
                                allyfleetcount = allyfleetcount + 1
                                friendfleetcount = friendfleetcount + 1
    
                                if self.hasRight('can_order_other_fleets') and fleet['shared']:
                                    fleet['fleetid'] = fleet['id']
    
                            elif fleet['relation'] == rFriend: friendfleetcount = friendfleetcount + 1
                            else: enemyfleetcount = enemyfleetcount + 1
                
                #---
                
                if planet['tag'] == None: planet['tag'] = ''
                
                if planet['floor'] == 0 and planet['space'] == 0:
                  
                    planet['empty'] = True

                    hasPlanetInfo = False
                    
                else:
                
                    hasPlanetInfo = True

                    p_img = 1 + (planet['floor'] + planet['id']) % 21
                    if p_img < 10: p_img = '0' + str(p_img)
                    else: p_img = str(p_img)

                    planet['planet_img'] = p_img

                #---
                
                planet['parked'] = 0                
                if planet['ground'] and (radarstrength > planet['radar_jamming'] or rel >= rAlliance or allyfleetcount > 0):
                    planet['parked'] = int(planet['ground'])

                if len(planet['fleets']) > 0 or planet['parked'] > 0:
                    planet['orbit'] = True

                #---
                
                if planet['ownerid'] == None:

                    displayPlanetInfo = radarstrength > 0 or allyfleetcount > 0
                    displayResources = displayPlanetInfo
                    displayElements = displayPlanetInfo

                    planet['ownerid'] = ''
                    planet['ownername'] = ''
                    planet['planetname'] = ''

                    if hasPlanetInfo: planet['uninhabited'] = True
                    
                else:
                
                    planet['ownerid'] = planet['ownerid']
                    planet['ownername'] = planet['username']

                    if rel == rSelf:
                    
                        planet['planetname'] = planet['name']
                        displayElements = True
                        displayPlanetInfo = True
                        displayResources = True
                        
                    elif rel == rAlliance:

                        planet['planetname'] = ''
                        displayElements = True
                        displayPlanetInfo = True
                        displayResources = True

                    elif rel == rFriend:
                    
                        planet['planetname'] = ''
                        displayElements = radarstrength > planet['radar_jamming'] or allyfleetcount > 0
                        displayPlanetInfo = displayElements
                        displayResources = radarstrength > 0 or allyfleetcount > 0
                        
                    else:
                        if radarstrength > 0 or allyfleetcount > 0:
                        
                            planet['planetname'] = planet['username']
                            displayElements = radarstrength > planet['radar_jamming'] or allyfleetcount > 0
                            displayPlanetInfo = displayElements
                            displayResources = radarstrength > 0 or allyfleetcount > 0
                            
                        else:
                        
                            planet['relation'] = -1
                            planet['tag'] = ''
                            planet['ownerid'] = ''
                            planet['ownername'] = ''
                            planet['planetname'] = ''
                            
                            displayElements = False
                            displayPlanetInfo = False
                            displayResources = False
                
                #---
                
                if rel >= rAlliance:
                
                    planet['radarstrength'] = planet['radar_strength']
                    planet['radarjamming'] = planet['radar_jamming']
                    
                else:
                    if radarstrength == 0:
                    
                        planet['radarstrength'] = -1
                        planet['radarjamming'] = 0
                        
                    elif planet['radar_jamming'] > 0:
                        if planet['radar_jamming'] >= radarstrength:
                        
                            planet['radarstrength'] = 1
                            planet['radarjamming'] = -1
                            
                        elif radarstrength > planet['radar_jamming']:
                        
                            planet['radarstrength'] = planet['radar_strength']
                            planet['radarjamming'] = planet['radar_jamming']
                        
                    elif planet['radar_strength'] == 0:
                    
                        planet['radarstrength'] = 0
                        planet['radarjamming'] = 0
                        
                    else:
                    
                        planet['radarstrength'] = planet['radar_strength']
                        planet['radarjamming'] = planet['radar_jamming']
                        
                #---
                
                if hasPlanetInfo and displayPlanetInfo:
                
                    planet['info'] = True
                    
                else:
                
                    planet['floor'] = ''
                    planet['space'] = ''
                    planet['noinfo'] = ''

                if displayResources and (planet['orbit_ore'] > 0 or planet['orbit_hydrocarbon'] > 0):
                
                    planet['ore'] = planet['orbit_ore']
                    planet['hydrocarbon'] = planet['orbit_hydrocarbon']
                    planet['resources'] = True
                    
                else:
                
                    planet['ore'] = 0
                    planet['hydrocarbon'] = 0
                    planet['noresources'] = True

                #---
                
                if displayElements and elementsArray:

                    planet['elements'] = []
                    for element in elementsArray:
                        if element['planetid'] == planet['id']:
                        
                            planet['elements'].append(element)
            
            #---
            
            tpl.set('galaxy_link')
            
            #---
            
            if radarstrength > 0:
                
                #---
                
                query = 'SELECT v.id, v.name, signature, speed, remaining_time,' + \
                        ' ownerid, owner_name, owner_relation, ' + \
                        ' planetid, planet_name, planet_galaxy, planet_sector, planet_planet,' + \
                        ' planet_ownerid, planet_owner_name, planet_owner_relation,' + \
                        ' destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, ' + \
                        ' destplanet_ownerid, destplanet_owner_name, destplanet_owner_relation, total_time,' + \
                        ' from_radarstrength, to_radarstrength, alliances.tag, radar_jamming, destplanet_radar_jamming' + \
                        ' FROM vw_fleets_moving v' + \
                        '    LEFT JOIN alliances ON alliances.id = owner_alliance_id' + \
                        ' WHERE userid=' + str(self.userId) + ' AND (' + \
                        '    (planetid >= sp_first_planet(' + str(galaxy) + ',' + str(sector) + ') AND planetid <= sp_last_planet(' + str(galaxy) + ',' + str(sector) + ')) OR' + \
                        '    (destplanetid >= sp_first_planet(' + str(galaxy) + ',' + str(sector) + ') AND destplanetid <= sp_last_planet(' + str(galaxy) + ',' + str(sector) + ')))' + \
                        ' ORDER BY remaining_time'
                results = dbRows(query)
                
                #---
                
                movings = []
                leavings = []
                enterings = []
                
                #---
                
                for result in results:
                    
                    #---
                    
                    relation = result['owner_relation']
                    loosing_time = -1

                    display_to = True
                    display_from = True

                    #---
                    
                    if relation <= rFriend:

                        radarSpotting = math.sqrt(radarstrength) * 6 * 1000 / result['speed'] * 3600

                        if result['from_radarstrength'] == 0:
                        
                            if result['remaining_time'] < radarSpotting: display_from = False
                            else: relation = -100
                            
                        elif result['to_radarstrength'] == 0:
                        
                            if result['total_time'] - result['remaining_time'] < radarSpotting:
                            
                                loosing_time = int(radarSpotting - (result['total_time'] - result['remaining_time']))
                                display_to = False
                                
                            else: relation = -100
                    
                    #---
                    
                    if relation > -100:
                        
                        #---
                        
                        fleet = {}

                        fleet['id'] = result['ownerid']
                        fleet['name'] = result['owner_name']

                        fleet['fleetid'] = result['id']
                        fleet['fleetname'] = result['name']
                        fleet['signature'] = result['signature']

                        #---
                        
                        if result['planet_galaxy'] == galaxy and result['planet_sector'] == sector:
                        
                            if result['destplanet_galaxy'] == galaxy and result['destplanet_sector'] == sector: movings.append(fleet)
                            else: leavings.append(fleet)
                            
                        else: enterings.append(fleet)
                        
                        #---
                        
                        if ((result['radar_jamming'] >= result['from_radarstrength'] and result['planet_owner_relation'] < rAlliance) or not display_from) and ((result['destplanet_radar_jamming'] >= result['to_radarstrength'] and result['destplanet_owner_relation'] < rAlliance) or not display_to) and result['owner_relation'] < rAlliance:
                            fleet['signature'] = 0

                        #---
                        
                        if loosing_time > -1:
                            fleet['time'] = loosing_time
                            fleet['losing'] = True
                        else:
                            fleet['time'] = result['remaining_time']
                        
                        #---
                        
                        if display_from:
                            fleet['f_planetname'] = self.getPlanetName(result['planet_owner_relation'], result['from_radarstrength'], result['planet_owner_name'], result['planet_name'])
                            fleet['f_planetid'] = result['planetid']
                            fleet['f_g'] = result['planet_galaxy']
                            fleet['f_s'] = result['planet_sector']
                            fleet['f_p'] = result['planet_planet']
                            fleet['f_relation'] = result['planet_owner_relation']
                        else:
                            fleet['f_planetname'] = ''
                            fleet['f_planetid'] = ''
                            fleet['f_g'] = ''
                            fleet['f_s'] = ''
                            fleet['f_p'] = ''
                            fleet['f_relation'] = '0'
                        
                        #---
                        
                        if display_to:
                            fleet['t_planetname'] = self.getPlanetName(result['destplanet_owner_relation'], result['to_radarstrength'], result['destplanet_owner_name'], result['destplanet_name'])
                            fleet['t_planetid'] = result['destplanetid']
                            fleet['t_g'] = result['destplanet_galaxy']
                            fleet['t_s'] = result['destplanet_sector']
                            fleet['t_p'] = result['destplanet_planet']
                            fleet['t_relation'] = result['destplanet_owner_relation']
                        else:
                            fleet['t_planetname'] = ''
                            fleet['t_planetid'] = ''
                            fleet['t_g'] = ''
                            fleet['t_s'] = ''
                            fleet['t_p'] = ''
                            fleet['t_relation'] = '0'
                        
                        #---
                        
                        fleet['relation'] = relation
                        
                        if result['tag']: fleet['alliancetag'] = result['tag']
                        else: fleet['alliancetag'] = ''

                #---
                
                tpl.set('movings', movings)
                tpl.set('enterings', enterings)
                tpl.set('leavings', leavings)

                #---
                
                tpl.set('radar') 
                
            #---
            
            return self.display(tpl, request)

    def getSector(self, sector, shiftX, shiftY):

        if (sector % 10 == 0) and (shiftX > 0): shiftX = 0
        if (sector % 10 == 1) and (shiftX < 0): shiftX = 0

        if (sector < 11) and (shiftY < 0): shiftY = 0
        if (sector > 90) and (shiftY > 0): shiftY = 0

        s = sector + shiftX + shiftY*10

        if s > 99: s = 99

        return s
