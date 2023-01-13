from .base import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        error = ''
        action = self.request.POST.get('action', '')
        
        if action == 'create':
            
            fleetname = self.request.POST.get('name', '').strip()
            if not isValidObjectName(fleetname):
                error = 'fleet_name_invalid'
            
            if error == '':
            
                dbRow = oConnRow('SELECT sp_create_fleet(' + str(self.UserId) + ',' + str(self.CurrentPlanet) + ',' + dosql(fleetname) + ') AS id')
                fleetid = dbRow['id']
                if fleetid < 0: error = 'fleet_too_many'
            
            if error == '':
            
                dbRows = oConnRows('SELECT id FROM db_ships')
                for dbRow in dbRows:
                    quantity = ToInt(self.request.POST.get('s' + str(dbRow['id'])), 0)
                    if quantity > 0:
                        oConnDoQuery('SELECT sp_transfer_ships_to_fleet(' + str(self.UserId) + ', ' + str(fleetid) + ', ' + str(dbRow['id']) + ', ' + str(quantity) + ')')
                oConnDoQuery('DELETE FROM fleets WHERE size=0 AND id=' + str(fleetid) + ' AND ownerid=' + str(self.UserId))
        
        #--- get
        
        self.selectedMenu = 'orbit'

        self.showHeader = True
        
        content = GetTemplate(self.request, 'planet-orbit')

        content.AssignValue('error', error)
        
        query = 'SELECT id, name, owner_name, signature, planet_owner_relation AS relation, action, engaged' + \
                ' FROM vw_fleets' + \
                ' WHERE planetid=' + str(self.CurrentPlanet) + ' AND action != 1 AND action != -1' + \
                ' ORDER BY upper(name)'
        dbRows = oConnRows(query)

        list = []
        content.AssignValue('fleets', list)
        
        for dbRow in dbRows:
            
            item = dbRow
            list.append(item)

        query = 'SELECT shipid AS id, quantity, label AS name' + \
                ' FROM planet_ships LEFT JOIN db_ships ON (planet_ships.shipid = db_ships.id)' + \
                ' WHERE planetid=' + str(self.CurrentPlanet) + \
                ' ORDER BY category, shipid'
        dbRows = oConnRows(query)
        
        list = []
        content.AssignValue('ships', list)
        
        for dbRow in dbRows:
            
            item = dbRow
            list.append(item)

        return self.Display(content)

