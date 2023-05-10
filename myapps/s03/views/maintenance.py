# -*- coding: utf-8 -*-

from myapps.s03.views._utils import *

class View(LoginRequiredMixin, View):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---
        
        if not maintenance: return HttpResponseRedirect('/')
        
        return super().dispatch(request, *args, **kwargs)
        
    ################################################################################

    def get(self, request, *args, **kwargs):
        
        #---

        tpl = getTemplate(request, 's03/maintenance')

        return render(request, tpl.template, tpl.data)
