from .lib import *


class View(ExileView):

    def get(self, request):
        
        data = {}
        
        data['main_tab'] = 'profile'
        data['profile_tab'] = 'overview'
        
        return self.display(request, 'ng0/profile_overview.html', data)
