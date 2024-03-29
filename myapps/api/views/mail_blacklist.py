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
                    
        if action == 'unignore':
        
            dbQuery('DELETE FROM messages_ignore_list WHERE userid=' + str(self.userId) + ' AND ignored_userid=(SELECT id FROM users WHERE lower(username)=lower(' + dosql(request.POST.get('user')) + '))')
            
        #---
            
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
            
        #---

        tpl = getTemplate()

        #---
        
        ignorednations = dbRows('SELECT ignored_userid AS userid, sp_get_user(ignored_userid) AS name, added, blocked FROM messages_ignore_list WHERE userid=' + str(self.userId))
        tpl.set('ignorednations', ignorednations)

        #---
        
        return Response(tpl.data)
