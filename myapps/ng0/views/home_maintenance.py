# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(LoginRequiredMixin, View):
    
    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):
        
        #---
        
        if not request.user.is_authenticated: return HttpResponseRedirect('/')

        if not maintenance: return HttpResponseRedirect('/ng0/')
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
    
        #---
        
        tpl = getTemplate(request, 'home-maintenance')
        
        return render(request, tpl.name, tpl.data)
