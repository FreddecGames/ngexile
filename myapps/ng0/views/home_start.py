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
        if not profile or profile['status'] != -3: return HttpResponseRedirect('/ng0/')
        
        #---
        
        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']):
        
            tpl = Template('home-closed')
            
            return tpl.render(request)
        
        #---
        
        return super().dispatch(request)

    ################################################################################
    
    def post(self, request):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'start':
        
            name = request.POST.get('name','').strip()
            if not isValidName(name):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
                
            try:
                dbQuery('UPDATE ng0.profiles SET username=' + strSql(name) + ' WHERE id=' + str(self.userId))
            except:
                messages.error(request, 'name_already_used')
                return HttpResponseRedirect(request.build_absolute_uri())

            galaxy = int(request.POST.get('galaxy', 0))
            result = dbExecute('SELECT ng0.profile_reset(' + str(self.userId) + ',' + str(galaxy) + ')')
            if result != 0:
                messages.error(request, 'profile_reset_error_' + result)
                return HttpResponseRedirect(request.build_absolute_uri())

            return HttpResponseRedirect('/ng0/home-wait/')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################

    def get(self, request):
        
        #---

        tpl = Template('home-start')

        #---
        
        galaxies = dbRows('SELECT * FROM ng0.vw_galaxies WHERE allow_new_players = true AND planet_count_for_new > 0')
        tpl.set('galaxies', galaxies)
        
        for galaxy in galaxies:
        
            if galaxy['protected'] and galaxy['planet_count_for_new'] > 50: galaxy['recommended'] = 1
            elif not galaxy['protected'] or galaxy['planet_count_for_new'] < 10: galaxy['recommended'] = -1
            else: galaxy['recommended'] = 0
        
        #---

        return tpl.render(request)
