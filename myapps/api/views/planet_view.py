# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'assigncommander':
        
            commander = ToInt(request.POST.get('commander'), 0)
            if ToInt(request.POST.get('commander'), 0) != 0: dbQuery('SELECT * FROM sp_commanders_assign(' + str(self.userId) + ',' + str(commander) + ',' + str(self.currentPlanetId) + ' ,null)')
            else: dbQuery('UPDATE nav_planet SET commanderid=null WHERE ownerid=' + str(self.userId) + ' AND id=' + str(self.currentPlanetId))
        
        #---
        
        elif action == 'rename':
        
            name = request.POST.get('name')
            if not isValidObjectName(name): messages.error(request, 'name_invalid')
            else: dbQuery('UPDATE nav_planet SET name=' + dosql(name) + ' WHERE ownerid=' + str(self.userId) + ' AND id=' + str(self.currentPlanetId))
        
        #---
        
        elif action == 'firescientists':
        
            amount = ToInt(request.POST.get('amount'), 0)
            dbQuery('SELECT sp_dismiss_staff(' + str(self.userId) + ',' + str(self.currentPlanetId) + ',' + str(amount) + ', 0, 0)')
        
        #---
        
        elif action == 'firesoldiers':
        
            amount = ToInt(request.POST.get('amount'), 0)
            dbQuery('SELECT sp_dismiss_staff(' + str(self.userId) + ',' + str(self.currentPlanetId) + ', 0,' + str(amount) + ', 0)')
        
        #---
        
        elif action == 'fireworkers':
        
            amount = ToInt(request.POST.get('amount'), 0)
            dbQuery('SELECT sp_dismiss_staff(' + str(self.userId) + ',' + str(self.currentPlanetId) + ', 0, 0,' + str(amount) + ')')
        
        #---
        
        elif action == 'abandon':
        
            dbQuery('SELECT sp_abandon_planet(' + str(self.userId) + ',' + str(self.currentPlanetId) + ')')
            return HttpResponseRedirect('/s03/empire-view/')
        
        #---
        
        elif action == 'resources_price':
        
            dbQuery('UPDATE nav_planet SET' + \
                    ' buy_ore = GREATEST(0, LEAST(1000, ' + str(ToInt(request.POST.get('buy_ore'), 0)) + ')),' + \
                    ' buy_hydrocarbon = GREATEST(0, LEAST(1000, ' + str(ToInt(request.POST.get('buy_hydrocarbon'), 0)) + '))' + \
                    ' WHERE ownerid=' + str(self.userId) + ' AND id=' + str(self.currentPlanetId))
            
        #---

        elif action == 'suspend':
        
            dbQuery('SELECT sp_update_planet_production(' + str(self.currentPlanetId) + ')')
            dbQuery('UPDATE nav_planet SET mod_production_workers=0, recruit_workers=False WHERE ownerid=' + str(self.userId) + ' AND id=' + str(self.currentPlanetId))
            
        #---
        
        elif action == 'resume':
        
            dbQuery('UPDATE nav_planet SET recruit_workers = True WHERE ownerid=' + str(self.userId) + ' AND id=' + str(self.currentPlanetId) )
            dbQuery('SELECT sp_update_planet(' + str(self.currentPlanetId) + ')')
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---

        tpl = getTemplate()
        
        self.showHeader = True
        
        #---
        
        query = 'SELECT id, name, fleetname, planetname, fleetid ' + \
                ' FROM vw_commanders' + \
                ' WHERE ownerid=' + str(self.userId) + \
                ' ORDER BY fleetid IS NOT NULL, planetid IS NOT NULL, fleetid, planetid'
        commanders = dbRows(query)

        cmd_groups = []
        tpl.set('optgroups', cmd_groups)
        
        cmd_nones = { 'typ':'none', 'cmds':[] }
        cmd_fleets = { 'typ':'fleet', 'cmds':[] }
        cmd_planets = { 'typ':'planet', 'cmds':[] }
        
        for cmd in commanders:

            if cmd['fleetname'] == None and cmd['planetname'] == None:
                cmd_nones['cmds'].append(cmd)
                
            elif cmd['fleetname'] == None:
                cmd_planets['cmds'].append(cmd)
                
            else:
                cmd_fleets['cmds'].append(cmd)
                activity = dbRow('SELECT dest_planetid, engaged, action FROM fleets WHERE ownerid=' + str(self.userId)+' AND id=' + str(cmd['fleetid']))
                if not (activity['dest_planetid'] == None and not activity['engaged'] and activity['action'] == 0):
                    cmd['unavailable'] = True

        if len(cmd_nones['cmds']) > 0: cmd_groups.append(cmd_nones)
        if len(cmd_fleets['cmds']) > 0: cmd_groups.append(cmd_fleets)
        if len(cmd_planets['cmds']) > 0: cmd_groups.append(cmd_planets)        
        
        #---
        
        query = 'SELECT id, name, galaxy, sector, planet, planet_floor, commanderid,' + \
                ' floor_occupied, floor, space_occupied, space,' + \
                ' workers, workers_capacity, scientists, scientists_capacity, soldiers, soldiers_capacity,' + \
                ' (mod_production_workers /10.0) AS growth, recruit_workers,' + \
                ' COALESCE(buy_ore, 0) AS buy_ore, COALESCE(buy_hydrocarbon, 0) AS buy_hydrocarbon' + \
                ' FROM vw_planets WHERE id=' + str(self.currentPlanetId)
        planet = dbRow(query)
        tpl.set('planet', planet)

        img = 1 + (planet['planet_floor'] + planet['id']) % 21
        if img < 10: img = '0' + str(img)
        planet['img'] = str(img)
        
        if planet['commanderid']:
            commander = dbRow('SELECT id, name FROM commanders WHERE ownerid=' + str(self.userId) + ' AND id=' + str(planet['commanderid']))
            planet['commander'] = commander
        
        #---
        
        query = 'SELECT buildingid, remaining_time, destroying, label' + \
                ' FROM vw_buildings_under_construction2' + \
                '  INNER JOIN db_buildings ON db_buildings.id=buildingid' + \
                ' WHERE planetid=' + str(self.currentPlanetId) + \
                ' ORDER BY remaining_time DESC'
        buildings = dbRows(query)
        tpl.set('buildings', buildings)
        
        #---
        
        query = 'SELECT shipid, remaining_time, recycle, label' + \
                ' FROM vw_ships_under_construction' + \
                '  INNER JOIN db_ships ON db_ships.id=shipid' + \
                ' WHERE ownerid=' + str(self.userId) + ' AND planetid=' + str(self.currentPlanetId) + ' AND end_time IS NOT NULL' + \
                ' ORDER BY remaining_time DESC'
        ships = dbRows(query)
        tpl.set('ships', ships)
        
        #---
        
        query = 'SELECT id, name, attackonsight, engaged, signature, action,' + \
                ' sp_relation(ownerid, ' + str(self.userId) + ') AS relation, sp_get_user(ownerid) AS ownername' + \
                ' FROM fleets' + \
                ' WHERE action != -1 AND action != 1 AND planetid=' + str(self.currentPlanetId) + \
                ' ORDER BY upper(name)'
        fleets = dbRows(query)
        tpl.set('fleets', fleets)
                
        #---
        
        return Response(tpl.data)
