from .base import *

class View(BaseView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        action = self.request.POST.get('action', '')
        
        if action == 'create':
            
            fleetname = self.request.POST.get('name', '').strip()
            if not isValidObjectName(fleetname):
                messages.error(request, 'create_fleet_error_name_invalid')
                return HttpResponseRedirect('/s03/planet-orbit/')
                
            dbRow = dbRow('SELECT sp_create_fleet(' + str(self.profile['id']) + ',' + str(self.currentPlanet['id']) + ',' + strSql(fleetname) + ') AS id')
            fleetid = dbRow['id']
            if fleetid < 0:
                messages.error(request, 'create_fleet_error_name_too_many')
                return HttpResponseRedirect('/s03/planet-orbit/')
            
            dbRows = dbRows('SELECT id FROM db_ships')
            for dbRow in dbRows:
                quantity = toInt(self.request.POST.get('s' + str(dbRow['id'])), 0)
                if quantity > 0:
                    dbRow = dbRow('SELECT sp_transfer_ships_to_fleet(' + str(self.profile['id']) + ', ' + str(fleetid) + ', ' + str(dbRow['id']) + ', ' + str(quantity) + ') AS result')
                    if dbRow['result'] != 0: messages.error(request, 'transfer_ships_to_fleet_error_' + str(dbRow['result']))
                    
            dbQuery('DELETE FROM fleets WHERE size=0 AND id=' + str(fleetid) + ' AND ownerid=' + str(self.profile['id']))
            return HttpResponseRedirect('/s03/planet-orbit/')
        
        #--- get
        
        self.selectedMenu = 'orbit'

        self.showHeader = True
        
        content = getTemplateContext(self.request, 'planet-orbit')
        
        # orbitting fleets
        
        query = 'SELECT id, name, owner_name, signature, planet_owner_relation AS relation, action, engaged' + \
                ' FROM vw_fleets' + \
                ' WHERE planetid=' + str(self.currentPlanet['id']) + ' AND action != 1 AND action != -1' + \
                ' ORDER BY upper(name)'
        dbRows = dbRows(query)

        list = []
        content.assignValue('fleets', list)
        
        for dbRow in dbRows:
            
            item = dbRow
            list.append(item)
        
        # ground ships
        
        query = 'SELECT shipid AS id, quantity, label AS name' + \
                ' FROM planet_ships LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id)' + \
                ' WHERE planetid=' + str(self.currentPlanet['id']) + \
                ' ORDER BY category, shipid'
        dbRows = dbRows(query)
        
        list = []
        content.assignValue('ships', list)
        
        for dbRow in dbRows:
            
            item = dbRow
            list.append(item)

        return self.display(content)

