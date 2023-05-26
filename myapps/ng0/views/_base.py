# -*- coding: utf-8 -*-

from myapps.ng0.views._utils import *


class BaseView(LoginRequiredMixin, View):

    ################################################################################
    
    def pre_dispatch(self, request):
        
        #--- 
        
        if not request.user.is_authenticated: return HttpResponseRedirect('/')

        self.userId = request.user.id
        
        if maintenance: return HttpResponseRedirect('/ng0/home-maintenance/')
        
        dbConnect()


class GameView(BaseView):

    showHeader = False
    headerUrl = None

    ################################################################################
    
    def pre_dispatch(self, request):
        
        #---
        
        response = super().pre_dispatch(request)
        if response: return response
        
        #---
        
        ipAddress = request.META.get('REMOTE_ADDR','')
        userAgent = request.META.get('HTTP_USER_AGENT','')
        forwardedFor = request.META.get('HTTP_X_FORWARDED_FOR','')
        
        dbQuery('SELECT ng0.profile_connect(' + str(self.userId) + ',' + strSql(ipAddress) + ',' + strSql(forwardedFor) + ',' + strSql(userAgent) + ')')

        if not request.user.is_impersonate:
            dbQuery('UPDATE ng0.profiles SET last_connection_date=now()')

        #---
        
        self.profile = dbRow('SELECT * FROM ng0.vw_profiles WHERE id=' + str(self.userId))

        if self.profile['status'] == -3: return HttpResponseRedirect('/ng0/home-start/')
        elif self.profile['status'] == -2: return HttpResponseRedirect('/ng0/home-wait/')
        elif self.profile['status'] == 0 and self.profile['planet_count'] <= 0: return HttpResponseRedirect('/ng0/home-gameover/')
        
        #---
        
        planetId = int(request.GET.get('planet', 0))        
        if planetId != 0 and planetId != self.profile['cur_planet_id']:

            planet = dbRow('SELECT id FROM ng0.planets WHERE floor_count > 0 AND space_count > 0 AND profile_id=' + str(self.userId) + ' AND id=' + str(planetId) + 'LIMIT 1')    
            if planet:

                self.profile['cur_planet_id'] = planet['id']
                if not request.user.is_impersonate:
                    dbQuery('UPDATE ng0.profiles SET cur_planet_id=' + str(planet['id']) + ' WHERE id=' + str(self.userId))
        
        #---
        
        if self.profile['cur_planet_id'] == None:
        
            planet = dbRow('SELECT id FROM ng0.planets WHERE floor_count > 0 AND space_count > 0 AND profile_id=' + str(self.userId) + ' LIMIT 1')    
            
            self.profile['cur_planet_id'] = planet['id']
            if not request.user.is_impersonate:
                dbQuery('UPDATE ng0.profiles SET cur_planet_id=' + str(planet['id']) + ' WHERE id=' + str(self.userId))

        #---

        self.curPlanet = dbRow('SELECT * FROM ng0.vw_planets WHERE id=' + str(self.profile['cur_planet_id']))

    ################################################################################
    
    def display(self, request, tpl):
    
        #---
        
        tpl.set('profile', self.profile)
        tpl.set('curPlanet', self.curPlanet)
        
        #---
        
        tpl.set('selectedTab', self.selectedTab)
        tpl.set('selectedMenu', self.selectedMenu)
        
        tpl.set('showHeader', self.showHeader)
        tpl.set('headerUrl', self.headerUrl)
        
        #---
        
        if request.user.is_impersonate:        
            tpl.set('impersonating')
            
        #---

        return tpl.render(request)
        