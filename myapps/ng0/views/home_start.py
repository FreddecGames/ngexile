# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(BaseView):
    
    ################################################################################
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        #---

        query = ' SELECT status' + \
                ' FROM ng0.profiles' + \
                ' WHERE id=' + str(self.userId)
        profile = dbRow(query)
        
        if not profile or profile['status'] != -2: return HttpResponseRedirect('/ng0/')
        
        #---
        
        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']):
        
            tpl = getTemplate(request, 'home-closed')
            return render(request, tpl.name, tpl.data)
    
    ################################################################################

    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, 'home-start')
                
        #---
        
        return render(request, tpl.name, tpl.data)
        