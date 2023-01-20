from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- get
        
        self.selectedMenu = 'fleets'

        content = getTemplateContext(self.request, 'fleets-idle')

        query = 'SELECT id, name, attackonsight' + \
                ' FROM vw_fleets WHERE ownerid=' + str(self.profile['id']) + \
                ' ORDER BY name'
        results = dbRows(query)
        fleets = results
        
        content.assignValue('fleets', fleets)

        return self.display(content)

