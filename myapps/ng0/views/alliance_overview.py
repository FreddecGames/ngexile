from .lib import *


class View(ExileView):

    def get(self, request):
        
        data = {}
        
        data['main_tab'] = 'alliance'
        data['alliance_tab'] = 'overview'
        
        return self.display(request, 'ng0/alliance_overview.html', data)
