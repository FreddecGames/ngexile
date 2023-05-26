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
    
    def post(self, request):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'rename':
        
            name = request.POST.get('name')
            if not isValidName(name):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            result = dbExecute('SELECT ng0.planet_rename(' + str(self.userId) + ',' + str(self.curPlanet['id']) + ',' + strSql(name) + ')')
            if result > 0:
                messages.error(request, 'planet_rename_error_' + str(result))
                return HttpResponseRedirect(request.build_absolute_uri())
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request):
        
        #---

        tpl = Template('planet-view')

        self.selectedTab = 'view'
        self.selectedMenu = 'planet'
        
        self.showHeader = True
        self.headerUrl = '/ng0/planet-view/'
                
        #---
        
        planet = dbRow('SELECT * FROM ng0.vw_planets WHERE id=' + str(self.curPlanet['id']))
        tpl.set('planet', planet)
                
        #---
        
        return self.display(request, tpl)
