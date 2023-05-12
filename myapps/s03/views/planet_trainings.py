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
    
    def post(self, request, *args, **kwargs):
    
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'train':
        
            trainSoldiers = ToInt(request.POST.get('soldiers'), 0)
            trainScientists = ToInt(request.POST.get('scientists'), 0)

            result = dbExecute('SELECT * FROM sp_start_training(' + str(self.userId) + ',' + str(self.currentPlanetId) + ',' + str(trainScientists) + ',' + str(trainSoldiers) + ')')

            if result == 5: messages.error(request, 'cant_train_now')
            elif result > 0: messages.error(request, 'not_enough_workers')
        
        #---
        
        elif action == 'cancel':
        
            queueId = ToInt(request.POST.get('q'), 0)
            if queueId != 0:
                dbQuery('SELECT * FROM sp_cancel_training(' + str(self.currentPlanetId) + ', ' + str(queueId) + ')')
                
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
    
    def get(self, request, *args, **kwargs):
    
        #---

        tpl = getTemplate(request, 'planet-trainings')

        self.selectedTab = 'trainings'
        self.selectedMenu = 'planet'

        self.showHeader = True
        self.headerUrl = '/s03/planet-trainings/'

        #---
        
        tpl.set('planetid', str(self.currentPlanetId))

        #---
        
        query = 'SELECT scientist_ore, scientist_hydrocarbon, scientist_credits,' + \
                ' soldier_ore, soldier_hydrocarbon, soldier_credits' + \
                ' FROM sp_get_training_price(' + str(self.userId) + ')'
        row = dbRow(query)
        
        tpl.set('prices', row)

        #---
        
        query = 'SELECT scientists, scientists_capacity, soldiers, soldiers_capacity, workers FROM vw_planets WHERE id=' + str(self.currentPlanetId)
        row = dbRow(query)
        
        tpl.set('planet', row)

        #---
        
        query = 'SELECT id, scientists, soldiers, int4(date_part(\'epoch\', end_time-now())) AS remainingtime' + \
                ' FROM planet_training_pending WHERE planetid=' + str(self.currentPlanetId) + ' AND end_time IS NOT NULL' + \
                ' ORDER BY start_time'
        rows = dbRows(query)

        tpl.set('trainings', rows)

        #---

        query = 'SELECT planet_training_pending.id, planet_training_pending.scientists, planet_training_pending.soldiers,' + \
                '    int4(ceiling(1.0*planet_training_pending.scientists/GREATEST(1, training_scientists)) * date_part(\'epoch\', INTERVAL \'1 hour\')) AS scientists_remainingtime,' + \
                '    int4(ceiling(1.0*planet_training_pending.soldiers/GREATEST(1, training_soldiers)) * date_part(\'epoch\', INTERVAL \'1 hour\')) AS soldiers_remainingtime' + \
                ' FROM planet_training_pending' + \
                '    JOIN nav_planet ON (nav_planet.id=planet_training_pending.planetid)' + \
                ' WHERE planetid=' + str(self.currentPlanetId) + ' AND end_time IS NULL' + \
                ' ORDER BY start_time'
        rows = dbRows(query)

        tpl.set('queues', rows)

        #---
        
        return self.display(tpl, request)
