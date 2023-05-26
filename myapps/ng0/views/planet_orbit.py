# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):
    
    ################################################################################
    
    def dispatch(self, request):
        
        #---

        response = super().pre_dispatch(request)
        if response: return response
        
        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def post(self, request):
    
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'create':

            name = request.POST.get('name')
            if not isValidName(name):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            fleetId = dbExecute('SELECT fleet_create(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + strSql(name) + ')')
            if fleetId < 0:
                messages.error(request, 'fleet_create_error_' + str(fleetId))
                return HttpResponseRedirect(request.build_absolute_uri())
            
            shipIds = dbRows('SELECT id FROM db_ships')
            for shipId in shipIds:
            
                count = int(request.POST.get('ship' + str(shipId['id']), 0))
                if count > 0:
                    
                    result = dbExecute('SELECT * FROM planet_ship_remove(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                    
                        dbQuery('DELETE FROM fleets WHERE id=' + str(fleetId) + ' AND profile_id=' + str(self.userId))
                        
                        messages.error(request, 'planet_ship_remove_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())
                        
                    result = dbExecute('SELECT * FROM fleet_add_ship(' + str(self.userId) + ',' + str(fleetId) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                    
                        dbQuery('DELETE FROM fleets WHERE id=' + str(fleetId) + ' AND profile_id=' + str(self.userId))
                        
                        messages.error(request, 'fleet_add_ship_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())
                
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
            
    ################################################################################
    
    def get(self, request):
        
        #---
        
        tpl = Template('planet-orbit')

        self.selectedTab = 'orbit'
        self.selectedMenu = 'planet'

        self.showHeader = True
        self.headerUrl = '/ng0/planet-orbit/'
        
        #---

        fleets = dbRows('SELECT * FROM vw_fleets WHERE planet_id=' + str(self.curPlanet['id']))        
        tpl.set('fleets', fleets)

        #---
        
        ships = dbRows('SELECT * FROM vw_planet_ships WHERE planet_id=' + str(self.curPlanet['id']))        
        tpl.set('ships', ships)
        
        #---

        return self.display(request, tpl)
