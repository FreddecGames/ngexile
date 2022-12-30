from .lib import *


class View(ExileView):

    def get(self, request):
        
        req_galaxy = request.GET.get('g', '')
        if req_galaxy == '':
            req_galaxy = self.curPlanet['galaxy']
        
        data = {}
        
        data['main_tab'] = 'map'
        
        data['cur_galaxy_id'] = req_galaxy
        
        query = 'SELECT id FROM ng0.galaxies ORDER BY id'
        data['galaxies'] = dbRows(query)
        
        query = 'SELECT ng0.planet_relation(id, ' + str(self.profile['id']) + ') AS relation FROM ng0.planets WHERE galaxy = ' + str(data['cur_galaxy_id']) + ' ORDER BY sector, number'
        data['planets'] = dbRows(query)
        
        return self.display(request, 'ng0/map_galaxy.html', data)
