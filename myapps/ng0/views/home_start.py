# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(BaseView):
    
    ################################################################################
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        #---

        query = ' SELECT status' + \
                ' FROM ng0.profiles' + \
                ' WHERE id=' + str(self.userId)
        profile = dbRow(query)
        
        if not profile or profile['status'] != -2: return HttpResponseRedirect('/ng0/')
        
        #---
        
        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']):
        
            tpl = getTemplate(request, 'home-closed')
            
            return render(request, tpl.name, tpl.data)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'start':

            username = request.POST.get('username', '').strip()
            if not isValidUsername(username):            
                messages.error(request, 'username_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())

            try:
                dbQuery('UPDATE ng0.profiles SET username=' + strSql(name) + ' WHERE id=' + str(self.userId))
            except:
                messages.error(request, 'username_already_used')
                return HttpResponseRedirect(request.build_absolute_uri())

            galaxy = int(request.POST.get('galaxy', 0))
            result = dbExecute('SELECT ng0.sp_profile_reset(' + str(self.userId) + ',' + str(galaxy) + ')')
            if result != 0:
                messages.error(request, 'profile_reset_error_' + result)
                return HttpResponseRedirect(request.build_absolute_uri())

            return HttpResponseRedirect('/ng0/home-wait/')

        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################

    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate(request, 'home-start')
        
        #---
        
        query = ' SELECT id, name, is_protected, planet_count, colony_count' + \
                ' FROM ng0.vw_galaxies' + \
                ' WHERE allow_new_player = true AND new_player_free_planet_count > 0'
        galaxies = dbRows(query)
        
        tpl.set('galaxies', galaxies)
        
        for item in galaxies:
        
            item['recommended'] = 0
            
            if item['colony_count'] > 0.66 * item['planet_count']: item['recommended'] = -1
            elif item['is_protected']: item['recommended'] = 1
        
        #---
        
        return render(request, tpl.name, tpl.data)
        