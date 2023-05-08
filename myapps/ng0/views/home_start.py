# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
    
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
        
        #---
        
        self.userId = request.user.id
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']):
            return HttpResponseRedirect('/ng0/start/')
        
        #---
            
        newName = request.POST.get('name', '').strip()
        if not isValidName(newName):
            messages.error(request, 'name_invalid')
            return HttpResponseRedirect('/ng0/start/')
        
        try:
            dbQuery('UPDATE users SET username=' + dosql(newName) + ' WHERE id=' + str(self.userId))
        except:
            messages.error(request, 'name_already_used')
            return HttpResponseRedirect('/ng0/start/')
        
        #---
            
        orientation = int(request.POST.get('orientation', 0))
        if not orientation:
            messages.error(request, 'orientation_invalid')
            return HttpResponseRedirect('/ng0/start/')
        
        dbQuery('UPDATE users SET orientation=' + str(orientation) + ' WHERE id=' + str(self.userId))
        
        if orientation == 1:
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',10,1)')
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',11,1)')
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',12,1)')

        elif orientation == 2:
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',20,1)')
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',21,1)')
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',22,1)')

        elif orientation == 3:
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',30,1)')
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',31,1)')
            dbQuery('INSERT INTO researches(userid, researchid, level) VALUES(' + str(self.userId) + ',32,1)')

        dbQuery('SELECT sp_update_researches(' + str(self.userId) + ')')
        
        #---
        
        galaxy = int(request.POST.get('galaxy', 0))
        result = dbExecute('SELECT sp_reset_account(' + str(self.userId) + ',' + str(galaxy) + ')')
        if result != 0:
            messages.error(request, 'reset_error_' + result[0])
            return HttpResponseRedirect('/ng0/start/')

        return HttpResponseRedirect('/ng0/wait/')
        
    def get(self, request, *args, **kwargs):

        if not registration['enabled'] or (registration['until'] != None and timezone.now() > registration['until']):
            tpl = getTemplate(request, 'ng0/start-closed')
            return render(request, tpl.template, tpl.data)
        
        #---

        tpl = getTemplate(request, 'ng0/start')

        galaxies = dbRows('SELECT id, recommended FROM sp_get_galaxy_info(' + str(self.userId) + ')')
        tpl.setValue('galaxies', galaxies)
        
        return render(request, tpl.template, tpl.data)
