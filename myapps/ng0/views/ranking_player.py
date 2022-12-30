from .lib import *


class View(ExileView):

    def get(self, request):
        
        data = {}
        
        data['main_tab'] = 'ranking'
        data['ranking_tab'] = 'player'
        
        return self.display(request, 'ng0/ranking_player.html', data)
