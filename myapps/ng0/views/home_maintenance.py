# -*- coding: utf-8 -*-

from myapps.ng0.views._utils import *

class View(LoginRequiredMixin, View):

    ################################################################################

    def dispatch(self, request):

        #---
        
        if not request.user.is_authenticated: return HttpResponseRedirect('/')
        
        if not maintenance: return HttpResponseRedirect('/ng0/')
        
        return super().dispatch(request)
        
    ################################################################################

    def get(self, request):
        
        #---

        tpl = Template('home-maintenance')

        return tpl.render(request)
