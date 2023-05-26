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
        
            shipIds = dbRows('SELECT id FROM db_ships')
            for shipId in shipIds:
            
                count = int(request.POST.get('ship' + str(shipId['id']), 0))
                if count > 0:
                
                    if count > 10000: count = 10000
                    
                    result = dbExecute('SELECT * FROM planet_ship_pending_create(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + str(shipId['id']) + ',' + str(count) + ')')
                    if result > 0:
                        messages.error(request, 'planet_ship_pending_create_error_' + str(result))
                        return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        elif action == 'cancel':
        
            queueId = int(request.POST.get('queue', 0))
            
            result = dbExecute('SELECT * FROM planet_ship_pending_cancel(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + str(queueId) + ')')
            if result > 0:
                messages.error(request, 'planet_ship_pending_cancel_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
                
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request):
    
        #---
        
        tpl = Template('planet-ships')
        
        self.selectedTab = 'ships'
        self.selectedMenu = 'planet'
        
        self.headerUrl = '/ng0/planet-ships/'
        self.showHeader = True

        #---

        pendings = dbRows('SELECT * FROM vw_planet_ship_pendings WHERE planet_id=' + str(self.curPlanet['id']))        
        tpl.set('pendings', pendings)
        
        #---
        
        ships = dbRows('SELECT * FROM vw_planet_ships WHERE planet_id=' + str(self.curPlanet['id']))        
        tpl.set('ships', ships)
        
        #---
        
        return self.display(request, tpl)
