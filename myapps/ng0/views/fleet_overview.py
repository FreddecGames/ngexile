from .lib import *


class View(ExileView):

    def get(self, request):
        
        data = {}
        
        data['main_tab'] = 'fleet'
        data['fleet_tab'] = 'overview'
        
        return self.display(request, 'ng0/fleet_overview.html', data)
