from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        action = self.request.POST.get('action', '')
        
        if action == 'train':
        
            soldiers = toInt(request.POST.get('soldiers'), 0)
            scientists = toInt(request.POST.get('scientists'), 0)            
            dbRow = dbRow('SELECT sp_start_training(' + str(self.profile['id']) + ',' + str(self.currentPlanet['id']) + ',' + str(scientists) + ',' + str(soldiers) + ') AS result')
            if dbRow['result'] != 0: messages.error(request, 'start_training_error_' + str(dbRow['result']))
            
            return HttpResponseRedirect('/s03/planet-trainings/')
            
        elif action == 'cancel':
        
            queueId = toInt(request.POST.get('q'), 0)
            dbRow = dbRow('SELECT sp_cancel_training(' + str(self.currentPlanet['id']) + ', ' + str(queueId) + ') AS result')
            if dbRow['result'] != 0: messages.error(request, 'cancel_training_error_' + str(dbRow['result']))
            
            return HttpResponseRedirect('/s03/planet-trainings/')
        
        #--- get
        
        self.selectedMenu = 'trainings'
        
        self.showHeader = True

        content = getTemplateContext(self.request, 'planet-trainings')
        
        # training prices
        
        query = 'SELECT scientist_ore, scientist_hydrocarbon, scientist_credits,' + \
                ' soldier_ore, soldier_hydrocarbon, soldier_credits' + \
                ' FROM sp_get_training_price(' + str(self.profile['id']) + ')'
        dbRow = dbRow(query)
        content.assignValue('price', dbRow)
        
        # current population
        
        query = 'SELECT scientists, scientists_capacity, soldiers, soldiers_capacity FROM vw_planets WHERE id=' + str(self.currentPlanet['id'])
        dbRow = dbRow(query)
        content.assignValue('pop', dbRow)

        # trainings in progress
        
        query = 'SELECT id, scientists, soldiers, int4(date_part(\'epoch\', end_time-now())) AS remainingtime' + \
                ' FROM planet_training_pending WHERE planetid=' + str(self.currentPlanet['id']) + ' AND end_time IS NOT NULL' + \
                ' ORDER BY start_time'
        dbRows = dbRows(query)

        list = []
        content.assignValue('trainings', list)
        
        for dbRow in dbRows:
            
            item = dbRow
            list.append(item)

        # trainings in queue
        
        query = 'SELECT planet_training_pending.id, planet_training_pending.scientists, planet_training_pending.soldiers,' + \
                '    int4(ceiling(1.0*planet_training_pending.scientists/GREATEST(1, training_scientists)) * date_part(\'epoch\', INTERVAL \'1 hour\')) AS remainingtimescientists,' + \
                '    int4(ceiling(1.0*planet_training_pending.soldiers/GREATEST(1, training_soldiers)) * date_part(\'epoch\', INTERVAL \'1 hour\')) AS remainingtimesoldiers' + \
                ' FROM planet_training_pending' + \
                '    JOIN nav_planet ON (nav_planet.id=planet_training_pending.planetid)' + \
                ' WHERE planetid=' + str(self.currentPlanet['id']) + ' AND end_time IS NULL' + \
                ' ORDER BY start_time'
        dbRows = dbRows(query)

        list = []
        content.assignValue('queues', list)
        
        for dbRow in dbRows:
            
            item = dbRow
            list.append(item)

        return self.display(content)
