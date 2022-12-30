from .lib import *


class View(ExileView):

    def get(self, request):
        
        data = {}
        
        data['main_tab'] = 'commander'
        data['commander_tab'] = 'overview'
        
        return self.display(request, 'ng0/commander_overview.html', data)
