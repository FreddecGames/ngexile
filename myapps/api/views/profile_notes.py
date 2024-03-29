# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################
    
    def post(self, request, *args, **kwargs):
    
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'save':
        
            notes = request.POST.get('notes', '').strip()
            if len(notes) <= 5100:
            
                dbQuery('UPDATE users SET notes=' + dosql(notes) + ' WHERE id = ' + str(self.userId))
                messages.success(request, 'done')
                
            else: messages.error(request, 'toolong')
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---
        
        tpl = getTemplate()

        #---

        tpl.set('maxlength', 5000)

        #---

        notes = dbExecute('SELECT notes FROM users WHERE id = ' + str(self.userId) + ' LIMIT 1' )
        tpl.set('data_notes', notes)

        #---
        
        return Response(tpl.data)
