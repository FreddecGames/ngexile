# -*- coding: utf-8 -*-

from myapps.ng0.views._utils import *

################################################################################

class BaseView(LoginRequiredMixin, View):
    
    def dispatch(self, request, *args, **kwargs):
    
        #---
        
        if not request.user.is_authenticated: return HttpResponseRedirect('/')
        
        if maintenance: return HttpResponseRedirect('/ng0/home-maintenance/')
        
        dbConnect()
        
        self.userId = request.user.id
        
        #---
        
        if hasattr(self.__class__, 'pre_dispatch'):
        
            response = self.pre_dispatch(request, *args, **kwargs)
            if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

################################################################################

class GetView(BaseView):
    
    show_planet_header = False
    
    tab_selected = ''
    menu_selected = ''
    
    template_name = ''
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        #---
        
        dbQuery('SELECT ng0.sp_profile_connect(' + str(self.userId) + ')')
        
        #---
        
        query = ' SELECT status, planet_count, cur_planet_id' + \
                ' FROM ng0.profiles' + \
                ' WHERE id=' + str(self.userId)
        self.profile = dbRow(query)

        if self.profile['status'] == -2: return HttpResponseRedirect('/ng0/home-start/')
        elif self.profile['status'] == -1: return HttpResponseRedirect('/ng0/home-wait/')
        elif self.profile['planet_count'] <= 0: return HttpResponseRedirect('/ng0/home-gameover/')
        
        #---
        
        planetId = int(request.GET.get('planet', 0))        
        if planetId != 0 and planetId != self.profile['cur_planet_id']:
        
            query = ' SELECT id, name, galaxy, sector, number' + \
                    ' FROM ng0.planets' + \
                    ' WHERE floor > 0 AND space > 0 AND id=' + str(planetId) + ' AND owner_id=' + str(self.userId)
            self.cur_planet = dbRow(query)
            
            if self.cur_planet and not request.user.is_impersonate:
            
                self.profile['cur_planet_id'] = planetId
                
                dbQuery('UPDATE ng0.profiles SET cur_planet_id=' + str(planetId) + ' WHERE id=' + str(self.userId))
                
        #---
        
        if self.profile['cur_planet_id'] == None or self.profile['cur_planet_id'] == '':

            query = ' SELECT id, name, galaxy, sector, number' + \
                    ' FROM ng0.planets' + \
                    ' WHERE floor > 0 AND space > 0 AND owner_id=' + str(self.userId) + ' LIMIT 1'
            self.cur_planet = dbRow(query)
            
            if self.cur_planet and not request.user.is_impersonate:
            
                self.profile['cur_planet_id'] = planetId
                
                dbQuery('UPDATE ng0.profiles SET cur_planet_id=' + str(planetId) + ' WHERE id=' + str(self.userId))
        
        #---
        
        if not self.cur_planet:
        
            query = ' SELECT id, name, galaxy, sector, number' + \
                    ' FROM ng0.planets' + \
                    ' WHERE floor > 0 AND space > 0 AND id=' + str(self.profile['cur_planet_id']) + ' AND owner_id=' + str(self.userId)
            self.cur_planet = dbRow(query)
        
        #---
        
        self.tpl = getTemplate(request, self.template_name)
        
    def get(self, request, *args, **kwargs):
    
        #---
        
        return self.render(request)
    
    def render(self, request):
        
        #---
        
        self.tpl.set('tab_selected', self.tab_selected)
        self.tpl.set('menu_selected', self.menu_selected)
        
        #---
        
        self.display(request, self.tpl)
        
        #---
        
        return render(request, self.tpl.name, self.tpl.data)

################################################################################

class GetPostView(GetView):
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action').strip().lower()

        response = self.process(request, self.tpl, action)
        if response: return response
        
        #---
        
        return self.render(request)
