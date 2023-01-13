from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        action = self.request.POST.get('action', '')
        
        if action == 'train':
        
            trainSoldiers = ToInt(request.POST.get('soldiers'), 0)
            trainScientists = ToInt(request.POST.get('scientists'), 0)            
            dbRow = oConnRow('SELECT sp_start_training(' + str(self.UserId) + ',' + str(self.CurrentPlanet) + ',' + str(trainScientists) + ',' + str(trainSoldiers) + ') AS result')
            if dbRow['result'] != 0: messages.error(request, 'training_error_' + str(dbRow['result']))
            
            return HttpResponseRedirect('/s03/planet-trainings/')
            
        elif action == 'cancel':
        
            queueId = ToInt(request.POST.get('q'), 0)
            oConnDoQuery('SELECT sp_cancel_training(' + str(self.CurrentPlanet) + ', ' + str(queueId) + ')')
            
            return HttpResponseRedirect('/s03/planet-trainings/')
        
        #--- get
        
        self.selectedMenu = 'trainings'
        
        self.showHeader = True

        content = GetTemplate(self.request, 'planet-trainings')
        
        # training prices
        
        query = 'SELECT scientist_ore, scientist_hydrocarbon, scientist_credits,' + \
                ' soldier_ore, soldier_hydrocarbon, soldier_credits' + \
                ' FROM sp_get_training_price(' + str(self.UserId) + ')'
        dbRow = oConnRow(query)
        content.AssignValue('price', dbRow)
        
        # current population
        
        query = 'SELECT scientists, scientists_capacity, soldiers, soldiers_capacity FROM vw_planets WHERE id=' + str(self.CurrentPlanet)
        dbRow = oConnRow(query)
        content.AssignValue('pop', dbRow)

        # trainings in progress
        
        query = 'SELECT id, scientists, soldiers, int4(date_part(\'epoch\', end_time-now())) AS remainingtime' + \
                ' FROM planet_training_pending WHERE planetid=' + str(self.CurrentPlanet) + ' AND end_time IS NOT NULL' + \
                ' ORDER BY start_time'
        dbRows = oConnRows(query)

        list = []
        content.AssignValue('trainings', list)
        
        for dbRow in dbRows:
            
            item = dbRow
            list.append(item)

        # trainings in queue
        
        query = 'SELECT planet_training_pending.id, planet_training_pending.scientists, planet_training_pending.soldiers,' + \
                '    int4(ceiling(1.0*planet_training_pending.scientists/GREATEST(1, training_scientists)) * date_part(\'epoch\', INTERVAL \'1 hour\')) AS remainingtimescientists,' + \
                '    int4(ceiling(1.0*planet_training_pending.soldiers/GREATEST(1, training_soldiers)) * date_part(\'epoch\', INTERVAL \'1 hour\')) AS remainingtimesoldiers' + \
                ' FROM planet_training_pending' + \
                '    JOIN nav_planet ON (nav_planet.id=planet_training_pending.planetid)' + \
                ' WHERE planetid=' + str(self.CurrentPlanet) + ' AND end_time IS NULL' + \
                ' ORDER BY start_time'
        dbRows = oConnRows(query)

        list = []
        content.AssignValue('queues', list)
        
        for dbRow in dbRows:
            
            item = dbRow
            list.append(item)

        return self.Display(content)
