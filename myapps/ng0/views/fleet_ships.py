# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):

    ################################################################################
    
    def dispatch(self, request, fleetId):

        #---

        response = super().pre_dispatch(request)
        if response: return response
        
        #---
        
        fleetId = int(request.GET.get('id', 0))
        if fleetId == 0:
            return HttpResponseRedirect('/ng0/')
        
        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def post(self, request, fleetId):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'transfer':

            shipIds = dbRows('SELECT id FROM db_ships')
            planetId = dbExecute('SELECT planetid FROM fleets WHERE id=' + str(fleetId))

            for shipId in shipIds:
            
                count = int(request.POST.get('addship' + str(shipId['id'])), 0)
                if count > 0:
                
                    result = dbExecute('SELECT fleet_ship_add(' + str(self.userId) + ',' + str(fleetId) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                        messages.error(request, 'fleet_ship_add_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())
                    
                    result = dbExecute('SELECT planet_ship_remove(' + str(self.userId) + ',' + str(fleetId) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                        messages.error(request, 'fleet_ship_add_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())

            for shipId in shipIds:
            
                count = int(request.POST.get('removeship' + str(shipId['id'])), 0)
                if count > 0:
                
                    result = dbExecute('SELECT fleet_ship_remove(' + str(self.userId) + ',' + str(fleetId) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                        messages.error(request, 'fleet_ship_remove_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())
                    
                    result = dbExecute('SELECT planet_ship_add(' + str(self.userId) + ',' + str(fleetId) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                        messages.error(request, 'planet_ship_add_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())

        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, fleetId):

        #---
        
        tpl = Template('fleet-ships')

        self.selectedTab = 'ships'
        self.selectedMenu = 'fleet'

        #---

        fleet = dbRows('SELECT * FROM vw_fleets WHERE id=' + str(fleetId))        
        tpl.set('fleet', fleet)

        #---

        fleetShips = dbRows('SELECT * FROM vw_fleet_ships WHERE fleet_id=' + str(fleetId))        
        tpl.set('fleetShips', fleetShips)
        
        #---

        planetShips = dbRows('SELECT * FROM vw_planet_ships WHERE planet_id=' + str(fleet['planet_id']))        
        tpl.set('planetShips', planetShips)
        
        #---
        
        return self.display(request, tpl)
