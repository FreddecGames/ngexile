# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(GameView):
    
    ################################################################################
    
    def dispatch(self, request):

        #---

        response = super().pre_dispatch(request)
        if response: return response

        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def get(self, request):
        
        #---
        
        tpl = Template('report-list')
        
        self.selectedTab = 'list'
        self.selectedMenu = 'report'

        #---

        reports = dbRows('SELECT * FROM ng0.vw_profile_reports WHERE profile_id=' + str(self.userId))        
        tpl.set('reports', reports)
        
        #---
        
        if not request.user.is_impersonate:
            dbQuery('UPDATE profile_reports SET reading_date = now() WHERE profile_id = ' + str(self.userId) + ' AND reading_date is null AND creation_date <= now()')

        #---

        return self.display(request, tpl)
