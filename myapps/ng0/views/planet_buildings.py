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
        
        if action == 'build':
        
            buildingId = int(request.POST.get('building', 0))
            
            result = dbExecute('SELECT * FROM planet_building_pending_create(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + str(buildingId) + ')')
            if result > 0:
                messages.error(request, 'planet_building_pending_create_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        elif action== 'destroy':
        
            buildingId = int(request.POST.get('building', 0))
            
            result = dbExecute('SELECT * FROM planet_building_delete(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + str(buildingId) + ')')
            if result > 0:
                messages.error(request, 'planet_building_delete_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
            
        #---
        
        elif action== 'cancel':
        
            queueId = int(request.POST.get('queue', 0))
            
            result = dbExecute('SELECT * FROM planet_building_pending_cancel(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + str(queueId) + ')')
            if result > 0:
                messages.error(request, 'planet_building_pending_cancel_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())        
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
            
    ################################################################################
    
    def get(self, request):
        
        #---
        
        tpl = Template('planet-buildings')
        
        self.selectedTab = 'buildings'
        self.selectedMenu = 'planet'        
        
        self.showHeader = True
        self.headerUrl = '/ng0/planet-buildings/'
                        
        #---

        pendings = dbRows('SELECT * FROM vw_planet_building_pendings WHERE planet_id=' + str(self.curPlanet['id']))        
        tpl.set('pendings', pendings)
        
        #---
        
        buildings = dbRows('SELECT * FROM vw_planet_buildings WHERE planet_id=' + str(self.curPlanet['id']))        
        tpl.set('buildings', buildings)
        
        #---
        
        return self.display(request, tpl)
