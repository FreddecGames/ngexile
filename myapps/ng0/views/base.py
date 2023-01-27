from myapps.ng0.views.utils import *


class BaseView(LoginRequiredMixin, View):
    
    profile = None
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        dbConnect()
    
    def display(self, tpl):
    
        return render(self.request, tpl.template, tpl.data)