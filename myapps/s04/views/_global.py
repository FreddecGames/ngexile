# -*- coding: utf-8 -*-

from myapps.s04.views._utils import *

class GlobalView(BaseView):

    selectedTab = ''
    selectedMenu = ''
    
    ################################################################################
    
    def pre_dispatch(self, request, *args, **kwargs):

        #---
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---

        dbQuery('SELECT * FROM s04.sp_profile_connect(' + str(self.userId) + ')')

        query = 'SELECT * FROM s04.vw_profiles' + \
                ' WHERE id=' + str(self.userId)
        self.profile = dbRow(query)

        if self.profile['status'] == 'new': return HttpResponseRedirect('/s04/home-start/')
        
        #---

        query = 'SELECT * FROM s04.vw_planets' + \
                ' WHERE id=' + str(self.profile['planet_id'])
        self.current_planet = dbRow(query)

    ################################################################################
    
    def display(self, tpl, request):
        
        #---

        tpl.set('selectedTab', self.selectedTab)
        tpl.set('selectedMenu', self.selectedMenu)

        tpl.set('profile', self.profile)
        tpl.set('current_planet', self.current_planet)

        #---
        
        return render(request, tpl.template, tpl.data)
