from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- get
        
        
        self.selectedMenu = 'fleets'

        content = getTemplateContext(self.request, 'empire-fleets')
        
        # filter
        
        filter = request.GET.get('filter', 'all')
        
        content.assignValue('filter', filter)

        # fleets
        
        query = 'SELECT id, name, attackonsight, commanderid, commandername, signature, size, engaged, action, remaining_time,' + \
                ' planet_galaxy, planet_sector, planet_planet, planet_owner_relation,' + \
                ' destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_owner_relation,' + \
                ' int4(cargo_ore + cargo_hydrocarbon + cargo_scientists + cargo_soldiers + cargo_workers) AS cargo' + \
                ' FROM vw_fleets WHERE ownerid=' + str(self.profile['id']) + \
                ' ORDER BY name'
        results = dbRows(query)
        
        if filter == 'all': fleets = results
        else:
            
            fleets = []
            for result in results:
                if result['engaged'] and filter == 'fighting': fleets.append(result)
                elif result['action'] == 0 and filter == 'idling': fleets.append(result)
                elif result['action'] == 1 and filter == 'moving': fleets.append(result)
                elif result['action'] == 2 and filter == 'recycling': fleets.append(result)
                elif result['action'] == 4 and filter == 'waiting': fleets.append(result)
        
        content.assignValue('fleets', fleets)

        # counter
        
        counter = { 'all':0, 'idling':0, 'moving':0, 'recycling':0, 'waiting':0, 'fighting':0 }
        
        for fleet in results:
            
            counter['all'] += 1
            
            if fleet['engaged']: counter['fighting'] += 1
            elif fleet['action'] == 0: counter['idling'] += 1
            elif fleet['action'] == 1: counter['moving'] += 1
            elif fleet['action'] == 2: counter['recycling'] += 1
            elif fleet['action'] == 4: counter['waiting'] += 1
        
        content.assignValue('counter', counter)

        return self.display(content)

