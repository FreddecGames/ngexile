# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):
    
    ################################################################################
    
    def dispatch(self, request, fleetId):

        #---

        response = super().pre_dispatch(request)
        if response: return response
        
        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def post(self, request, fleetId):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'rename':
        
            name = request.POST.get('name')
            if not isValidName(name):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            result = dbExecute('SELECT * FROM fleet_rename(' + str(self.userId) + ',' + str(fleetId) + ',' + strSql(name) + ')')
            if result > 0:
                messages.error(request, 'fleet_rename_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
            
        #---
        
        elif action == 'move':
        
            g = int(request.POST.get('galaxy', -1)
            s = int(request.POST.get('sector', -1)
            n = int(request.POST.get('number', -1)
            
            if g == -1 or s == -1 or n == -1:
                messages.error(request, 'bad_destination')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            result = dbExecute('SELECT fleet_move(' + str(self.userId) + ',' + str(fleetId) + ',' + str(g) + ',' + str(s) + ',' + str(n) + ')')
            if result > 0:
                messages.error(request, 'fleet_move_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
                
            moveType = request.POST.get('movetype')
            
            if moveType == '1':
            
                result = dbExecute('SELECT fleet_waypoint_add_unloadall(' + str(self.userId) + ',' + str(fleetId) + ')')
                if result > 0:
                    messages.error(request, 'fleet_waypoint_add_unloadall_error_' + str(result))
                    return HttpResponseRedirect(request.build_absolute_uri())
            
            elif moveType == '2':
            
                result = dbExecute('SELECT fleet_waypoint_add_recycle(' + str(self.userId) + ',' + str(fleetId) + ')')
                if result > 0:
                    messages.error(request, 'fleet_waypoint_add_recycle_error_' + str(result))
                    return HttpResponseRedirect(request.build_absolute_uri())
            
        #---
        
        elif action == 'transfer':
        
            ore = int(request.POST.get('load_ore', 0)) - int(request.POST.get('unload_ore', 0))
            hydro = int(request.POST.get('load_hydro', 0)) - int(request.POST.get('unload_hydro', 0))
            scientist = int(request.POST.get('load_scientists', 0)) - int(request.POST.get('unload_scientists', 0))
            soldier = int(request.POST.get('load_soldiers', 0)) - int(request.POST.get('unload_soldiers', 0))
            worker = int(request.POST.get('load_workers', 0)) - int(request.POST.get('unload_workers', 0))
        
            if ore != 0 or hydro != 0 or scientists != 0 or soldiers != 0 or workers != 0:
            
                result = dbExecute('SELECT fleet_transfer_resources_with_planet(' + str(self.userId) + ',' + str(fleetId) + ',' + str(ore) + ',' + str(hydro) + ',' + str(scientists) + ',' + str(soldiers) + ',' + str(workers) + ')')
                if result > 0:
                    messages.error(request, 'fleet_transfer_resources_with_planet_error_' + str(result))
                    return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        elif action == 'leave':
            
            result = dbExecute('SELECT fleet_leave(' + str(self.userId) + ',' + str(fleetId) + ')')
            if result > 0:
                messages.error(request, 'fleet_leave_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        elif action == 'attack':
            
            result = dbExecute('SELECT fleet_stance_attack(' + str(self.userId) + ',' + str(fleetId) + ')')
            if result > 0:
                messages.error(request, 'fleet_stance_attack_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        elif action == 'ripost':
            
            result = dbExecute('SELECT fleet_stance_ripost(' + str(self.userId) + ',' + str(fleetId) + ')')
            if result > 0:
                messages.error(request, 'fleet_stance_ripost_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        elif action == 'startrecycling':
        
            result = dbExecute('SELECT fleet_start_recycling(' + str(self.userId) + ',' + str(fleetId) + ')')
            if result > 0:
                messages.error(request, 'fleet_start_recycling_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        elif action == 'stoprecycling':
        
            result = dbExecute('SELECT fleet_stop_recycling(' + str(self.userId) + ',' + str(fleetId) + ')')
            if result > 0:
                messages.error(request, 'fleet_stop_recycling_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
            
        elif action == 'stopwaiting':
        
            result = dbExecute('SELECT fleet_stop_waiting(' + str(self.userId) + ',' + str(fleetId) + ')')
            if result > 0:
                messages.error(request, 'fleet_stop_waiting_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
            
        elif action == 'merge':
        
            withId = int(request.POST.get('with', 0))
            if withId > 0:
            
                result = dbExecute('SELECT fleet_merge(' + str(self.userId) + ',' + str(fleetId) + ',' + str(withId) + ')')
                if result > 0:
                    messages.error(request, 'fleet_merge_error_' + str(result))
                    return HttpResponseRedirect(request.build_absolute_uri())
            
        #---
            
        elif action == 'return':
        
            result = dbExecute('SELECT fleet_return(' + str(self.userId) + ',' + str(fleetId) + ')')
            if result > 0:
                messages.error(request, 'fleet_return_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
            
        elif action == 'deploy':
        
            shipId = int(request.POST.get('ship', 0))
            if shipId > 0:
            
                result = dbExecute('SELECT fleet_deploy(' + str(self.userId) + ',' + str(fleetId) + ',' + str(shipId) + ')')
                if result > 0:
                    messages.error(request, 'fleet_return_error_' + str(result))
                    return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, fleetId):
        
        #---
        
        tpl = Template('fleet-view')
        
        self.selectedTab = 'view'
        self.selectedMenu = 'fleet'
                
        #---

        fleet = dbRows('SELECT * FROM vw_fleets WHERE id=' + str(fleetId))        
        tpl.set('fleet', fleet)
        
        #---

        actions = dbRows('SELECT * FROM vw_fleet_actions WHERE fleet_id=' + str(fleetId))        
        tpl.set('actions', actions)
                
        #---

        ships = dbRows('SELECT * FROM vw_fleet_ships WHERE fleet_id=' + str(fleetId))        
        tpl.set('ships', ships)
        
        #---
        
        if fleet['planet_id']:
        
            fleets = dbRows('SELECT * FROM vw_fleets WHERE planet_id=' + str(fleet['planet_id']))        
            tpl.set('fleets', fleets)
        
        #---
        
        return self.display(request, tpl)
