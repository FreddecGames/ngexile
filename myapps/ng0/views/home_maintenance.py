# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):
        
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):
        
        #---

        self.tpl = getTemplate(request, "ng0/maintenance")
        
        #---

        return render(request, self.tpl.template, self.tpl.data)
