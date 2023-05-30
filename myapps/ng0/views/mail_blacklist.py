# -*- coding: utf-8 -*-

from myapps.ng0.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
                    
        if action == 'unignore':
        
            dbQuery('DELETE FROM messages_ignore_list WHERE userid=' + str(self.userId) + ' AND ignored_userid=(SELECT id FROM users WHERE lower(username)=lower(' + dosql(request.POST.get('user')) + '))')
            
        #---
            
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
            
        #---

        tpl = getTemplate(request, 'mail-blacklist')
                
        self.selectedTab = 'blacklist'
        self.selectedMenu = 'mails'

        #---
        
        ignorednations = dbRows('SELECT ignored_userid AS userid, sp_get_user(ignored_userid) AS name, added, blocked FROM messages_ignore_list WHERE userid=' + str(self.userId))
        tpl.set('ignorednations', ignorednations)

        #---
        
        return self.display(tpl, request)
