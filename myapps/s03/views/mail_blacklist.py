# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        
        #---
                    
        if request.POST.get("a", "") == "unignore":
        
            dbQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.userId) + " AND ignored_userid=(SELECT id FROM users WHERE lower(username)=lower(" + dosql(request.POST.get("user")) + "))")
            
        #---
            
        return HttpResponseRedirect('/s03/mail-blacklist/')
        
    def get(self, request, *args, **kwargs):
            
        #---
                
        self.selectedMenu = "mails"

        content = getTemplate(request, "s03/mail-ignorelist")

        #---
        ignorednations = dbRows("SELECT ignored_userid AS userid, sp_get_user(ignored_userid) AS name, added, blocked FROM messages_ignore_list WHERE userid=" + str(self.userId))
        content.setValue("ignorednations", ignorednations)

        return self.display(content, request)
