# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(BaseView):

    ################################################################################

    def dispatch(self, request):

        #---

        response = super().pre_dispatch(request)
        if response: return response
        
        #---
        
        profile = dbRow('SELECT * FROM ng0.vw_profiles WHERE id=' + str(self.userId))        
        if not profile or profile['planet_count'] > 0: return HttpResponseRedirect('/ng0/')
        
        #---
        
        return super().dispatch(request)

    ################################################################################

    def post(self, request):

        #---
        
        action = request.POST.get('action')

        #---

        if action == 'retry':
            
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
        
        elif action == 'delete':
        
            dbQuery('UPDATE ng0.profiles SET deletion_date = now() WHERE id=' + str(self.userId))
            return HttpResponseRedirect('/')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
        
    def get(self, request):

        #---
        
        tpl = Template('home-gameover')
        
        #---
        
        profile = dbRow('SELECT * FROM ng0.vw_profiles WHERE id=' + str(self.userId))        
        tpl.set('profile', profile)

        #---

        galaxies = dbRows('SELECT * FROM ng0.vw_galaxies WHERE new_planets > 0')
        tpl.set('galaxies', galaxies)

        #---

        return tpl.render(request)
