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
        
            soldierCount = int(request.POST.get('soldier', 0))
            scientistCount = int(request.POST.get('scientist', 0))

            result = dbExecute('SELECT * FROM planet_training_pending_create(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + str(scientistCount) + ',' + str(soldierCount) + ')')
            if result > 0:
                messages.error(request, 'planet_training_pending_create_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        elif action == 'cancel':
        
            queueId = int(request.POST.get('queue', 0))
            
            result = dbExecute('SELECT * FROM planet_training_pending_cancel(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + str(queueId) + ')')
            if result > 0:
                messages.error(request, 'planet_training_pending_cancel_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request):
    
        #---

        tpl = Template('planet-trainings')

        self.selectedTab = 'trainings'
        self.selectedMenu = 'planet'

        self.showHeader = True
        self.headerUrl = '/ng0/planet-trainings/'

        #---

        pendings = dbRows('SELECT * FROM vw_planet_training_pendings WHERE planet_id=' + str(self.curPlanet['id']))        
        tpl.set('pendings', pendings)
        
        #---
        
        trainings = dbRows('SELECT * FROM vw_planet_trainings WHERE planet_id=' + str(self.curPlanet['id']))        
        tpl.set('trainings', trainings)

        #---
        
        return self.display(request, tpl)
