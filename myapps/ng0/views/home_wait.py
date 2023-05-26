# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(BaseView):

    ################################################################################

    def dispatch(self, request):

        #---

        response = super().pre_dispatch(request)
        if response: return response
            
        #---
        
        profile = dbRow('SELECT * FROM ng0.profiles WHERE id=' + str(self.userId))        
        if not profile or profile['status'] != -2: return HttpResponseRedirect('/ng0/')
        
        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def post(self, request):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'unlock':
        
            dbQuery('UPDATE ng0.profiles SET status = 0 WHERE id=' + str(self.userId))
            return HttpResponseRedirect('/ng0/')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request):

        #---

        tpl = Template('home-wait')

        #---

        profile = dbRow('SELECT * FROM ng0.vw_profiles WHERE id=' + str(self.userId))        
        tpl.set('profile', profile)
        
        #---
        
        return tpl.render(request)
