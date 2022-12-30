from .lib import *


class View(ExileView):

    def get(self, request):
        
        data = {}
        
        data['main_tab'] = 'planet'
        data['planet_tab'] = 'buildings'
        
        query = 'SELECT * FROM ng0.planets WHERE profile_id=' + str(self.profile['id']) + ' ORDER BY galaxy, sector, number'
        data['planets'] = dbRows(query)
        
        return self.display(request, 'ng0/planet_buildings.html', data)
