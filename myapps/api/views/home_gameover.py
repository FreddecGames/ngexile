# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsNotInMaintenance, IsGameover ]

    ################################################################################

    def post(self, request, *args, **kwargs):

        #---
        
        action = request.data['action']

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
        
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    ################################################################################
        
    def get(self, request, *args, **kwargs):

        #---
        
        tpl = getTemplate()
        
        #---
        
        query = 'SELECT username, planets, credits_bankruptcy' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        row = dbRow(query)
        
        tpl.set('profile', row)

        #---

        query = 'SELECT id, recommended' + \
                ' FROM sp_get_galaxy_info(' + str(self.userId) + ')'
        rows = dbRows(query)
        
        tpl.set('galaxies', rows)

        #---

        return Response(tpl.data)
