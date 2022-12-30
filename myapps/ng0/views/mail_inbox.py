from .lib import *


class View(ExileView):

    def get(self, request):
        
        data = {}
        
        data['main_tab'] = 'mail'
        data['mail_tab'] = 'inbox'
        
        return self.display(request, 'ng0/mail_inbox.html', data)
