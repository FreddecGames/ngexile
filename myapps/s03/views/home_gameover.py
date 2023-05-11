# -*- coding: utf-8 -*-

from myapps.s03.views._utils import *

class View(BaseView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        query = 'SELECT planets, credits_bankruptcy' + \
                'FROM users' + \
                'WHERE id=' + str(self.userId)
        row = dbRow(query)
        
        if not row or (row['planets'] > 0 and row['credits_bankruptcy'] > 0): return HttpResponseRedirect('/s03/')
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################

    def post(self, request, *args, **kwargs):

        #---
        
        action = request.POST.get('action')

        #---

        if action == 'retry':
            
            username = request.POST.get('name', '')
            if not isValidName(username):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect(request.build_absolute_uri())
                
            try:
                dbQuery('UPDATE users SET alliance_id=NULL, username=' + dosql(username) + ' WHERE id=' + str(self.userId))
            except:
                messages.error(request, 'name_already_used')
                return HttpResponseRedirect(request.build_absolute_uri())

            result = dbExecute('SELECT sp_reset_account(' + str(self.userId) + ',' + str(ToInt(request.POST.get('galaxy'), 1)) + ')')
            if result == 0:
                return HttpResponseRedirect('/s03/empire-view/')

            messages.error(request, 'error_' + result)
            return HttpResponseRedirect(request.build_absolute_uri())

        #---
        
        elif action == 'abandon':
        
            dbQuery('UPDATE users SET deletion_date=now() WHERE id=' + str(self.userId))
            return HttpResponseRedirect('/')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())

    ################################################################################
        
    def get(self, request, *args, **kwargs):

        #---
        
        tpl = getTemplate(request, 'home-gameover')
        
        #---
        
        query = 'SELECT username, planets, credits_bankruptcy' + \
                'FROM users' + \
                'WHERE id=' + str(self.userId)
        row = dbRow(query)
        
        tpl.set('profile', row)

        #---

        query = 'SELECT id, recommended' + \
                'FROM sp_get_galaxy_info(' + str(self.userId) + ')'
        rows = dbRows(query)
        
        tpl.set('galaxies', rows)

        #---

        return render(request, tpl.template, tpl.data)
