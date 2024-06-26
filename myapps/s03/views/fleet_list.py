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
        
        action = request.GET.get('action')
        
        #---
        
        if action == 'setcat':
            
            fleetId = ToInt(request.GET.get('id'), 0)
            oldCat = ToInt(request.GET.get('old'), 0)
            newCat = ToInt(request.GET.get('new'), 0)

            result = dbExecute('SELECT sp_fleets_set_category(' + str(self.userId) + ',' + str(fleetId) + ',' + str(oldCat) + ',' + str(newCat) + ')')
            if result:
            
                tpl = getTemplate(request, 'fleet-list')

                tpl.set('id', fleetId)
                tpl.set('old', oldCat)
                tpl.set('new', newCat)
                
                tpl.set('fleet_category_changed')

                return render(request, tpl.template, tpl.data)

            return HttpResponseRedirect('/s03/fleet-list/')
            
        #---
        
        elif action == 'newcat':
        
            name = request.GET.get('name')

            if isValidCategoryName(name):
            
                result = dbExecute('SELECT sp_fleets_categories_add(' + str(self.userId) + ',' + dosql(name) + ')')                
                if result:
                    
                    tpl = getTemplate(request, 'fleet-list')
                    
                    tpl.set('id', result)
                    tpl.set('label', name)
                    tpl.set('category')

                    return render(request, tpl.template, tpl.data)

            else:
            
                tpl = getTemplate(request, 'fleet-list')
                
                tpl.set('category_name_invalid')

                return render(request, tpl.template, tpl.data)

            return HttpResponseRedirect('/s03/fleet-list/')
                
        #---
        
        elif action == 'rencat':
        
            name = request.GET.get('name')
            catid = ToInt(request.GET.get('id'), 0)

            if name == '':
            
                result = dbExecute('SELECT sp_fleets_categories_delete(' + str(self.userId) + ',' + str(catid) + ')')
                if result:

                    tpl = getTemplate(request, 'fleet-list')
                    
                    tpl.set('id', catid)
                    tpl.set('label', name)
                    tpl.set('category')

                    return render(request, tpl.template, tpl.data)

            elif isValidCategoryName(name):
            
                result = dbExecute('SELECT sp_fleets_categories_rename(' + str(self.userId) + ',' + str(catid) + ',' + dosql(name) + ')')
                if result:
                    
                    tpl = getTemplate(request, 'fleet-list')
                    
                    tpl.set('id', catid)
                    tpl.set('label', name)
                    tpl.set('category')

                    return render(request, tpl.template, tpl.data)

            else:
                
                tpl = getTemplate(request, 'fleet-list')
                
                tpl.set('category_name_invalid')

                return render(request, tpl.template, tpl.data)

            return HttpResponseRedirect('/s03/fleet-list/')
                
        #---
        
        tpl = getTemplate(request, 'fleet-list')
        
        self.selectedMenu = 'fleet'
        
        #---

        query = 'SELECT category, label' + \
                ' FROM users_fleets_categories' + \
                ' WHERE userid=' + str(self.userId) + \
                ' ORDER BY upper(label)'
        categories = dbRows(query)
        tpl.set('categories', categories)
        
        #---

        query = 'SELECT fleetid, fleets_ships.shipid, quantity, label' + \
                ' FROM fleets' + \
                '    INNER JOIN fleets_ships ON (fleets.id=fleets_ships.fleetid)' + \
                '    INNER JOIN db_ships ON (db_ships.id=fleets_ships.shipid)' + \
                ' WHERE ownerid=' + str(self.userId) + \
                ' ORDER BY fleetid, fleets_ships.shipid'
        ships = dbRows(query)

        query = 'SELECT id, name, attackonsight, engaged, size, signature, speed, remaining_time, commanderid, commandername,' + \
                ' planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, planet_owner_relation,' + \
                ' destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_ownerid, destplanet_owner_name, destplanet_owner_relation,' + \
                ' cargo_capacity, cargo_load, cargo_ore, cargo_hydrocarbon, cargo_scientists, cargo_soldiers, cargo_workers,' + \
                ' recycler_output, orbit_ore > 0 OR orbit_hydrocarbon > 0, action,' + \
                '( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.planet_galaxy AND nav_planet.sector = f.planet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = ' + str(self.userId) + ')) AS from_radarstrength, ' + \
                '( SELECT int4(COALESCE(max(nav_planet.radar_strength), 0)) FROM nav_planet WHERE nav_planet.galaxy = f.destplanet_galaxy AND nav_planet.sector = f.destplanet_sector AND nav_planet.ownerid IS NOT NULL AND EXISTS ( SELECT 1 FROM vw_friends_radars WHERE vw_friends_radars.friend = nav_planet.ownerid AND vw_friends_radars.userid = ' + str(self.userId) + ')) AS to_radarstrength,' + \
                ' categoryid' + \
                ' FROM vw_fleets as f WHERE ownerid=' + str(self.userId)
        fleets = dbRows(query)
        tpl.set('fleets', fleets)

        for fleet in fleets:
        
            if fleet['engaged']: fleet['action'] = 'x'
            
            if fleet['attackonsight']: fleet['attackonsight'] = 1
            else: fleet['attackonsight'] = 0
            
            if not fleet['remaining_time']: fleet['remaining_time'] = 0
            
            if not fleet['destplanetid']: fleet['destplanetid'] = 0
            
            fleet['ships'] = []
            for ship in ships:
                if ship['fleetid'] == fleet['id']:
                    fleet['ships'].append(ship)

        #---
        
        return self.display(tpl, request)
