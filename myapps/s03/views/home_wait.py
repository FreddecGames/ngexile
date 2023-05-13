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
        
        if not row or row['privilege'] != -3 or row['resets'] == 0: return HttpResponseRedirect('/s03/')
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == 'unlock':
        
            dbQuery('UPDATE users SET privilege=0 WHERE id=' + str(self.userId))
            return HttpResponseRedirect('/s03/empire-view/')
        
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---

        tpl = getTemplate(request, 'home-wait')

        #---

        query = 'SELECT username' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        row = dbRow(query)

        tpl.set('profile', row)
        
        #---
        
        return render(request, tpl.template, tpl.data)
