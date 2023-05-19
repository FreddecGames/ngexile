# -*- coding: utf-8 -*-

from myapps.s03.views._utils import *

class View(BaseView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):
        
        #---
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
            
        #---
        
        query = 'SELECT privilege, resets' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        row = dbRow(query)
        
        if not row or row['privilege'] != -3 or row['resets'] != 0: return HttpResponseRedirect('/s03/')
        
        #---
        
        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']):
        
            tpl = getTemplate(request, 'home-closed')
            
            return render(request, tpl.template, tpl.data)
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'start':
                        
            name = request.POST.get('name', '').strip()
            if not isValidName(name):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            try:
                dbQuery('UPDATE users SET username=' + dosql(name) + ' WHERE id=' + str(self.userId))
            except:
                messages.error(request, 'name_already_used')
                return HttpResponseRedirect(request.build_absolute_uri())
                
            orientation = ToInt(request.POST.get('orientation'), 0)
            if orientation == 0:
                messages.error(request, 'orientation_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
            
            dbQuery('UPDATE users SET orientation=' + str(orientation) + ' WHERE id=' + str(self.userId))
            
            if orientation == 1:
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 10, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 11, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 12, 1)')

            elif orientation == 2:
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 20, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 21, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 22, 1)')

            elif orientation == 3:
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 30, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 31, 1)')
                dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ', 32, 1)')

            dbQuery('SELECT sp_update_researches(' + str(self.userId) + ')')
            
            galaxy = ToInt(request.POST.get('galaxy'), 0)
            result = dbExecute('SELECT sp_reset_account(' + str(self.userId) + ',' + str(galaxy) + ')')
            if result != 0:
                messages.error(request, 'reset_error_' + result)
                return HttpResponseRedirect(request.build_absolute_uri())

            return HttpResponseRedirect('/s03/home-wait/')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---

        tpl = getTemplate(request, 'home-start')

        #---
        
        query = 'SELECT id, recommended' + \
                ' FROM sp_get_galaxy_info(' + str(self.userId) + ')'
        rows = dbRows(query)
        
        tpl.set('galaxies', rows)
        
        #---
        
        return render(request, tpl.template, tpl.data)
