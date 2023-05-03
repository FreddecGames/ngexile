# -*- coding: utf-8 -*-

from myapps.ng0.views._utils import *

class BaseView(LoginRequiredMixin, View):
    
    def dispatch(self, request, *args, **kwargs):
    
        #---
        
        response = self.pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        return super().dispatch(request, *args, **kwargs)

class GetView(BaseView):
    
    template_name = ''
    
    def pre_dispatch(self, request, *args, **kwargs):
    
        #---
        
        self.tpl = getTemplate(request, self.template_name)
    
    def get(self, request, *args, **kwargs):
    
        #---
        
        return self.render(request)
    
    def render(self, request):
    
        #---
        
        self.display(request)
        
        #---
    
        return render(request, self.tpl.name, self.tpl.data)

class GetPostView(GetView):
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action').strip().lower()

        response = self.process(request, tpl, action)
        if response: return response
        
        #---
        
        return self.render(request)
