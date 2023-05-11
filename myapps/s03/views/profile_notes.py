# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

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
        
        if action == "save":
        
            notes = request.POST.get("notes", "").strip()
            if len(notes) <= 5100:
            
                dbQuery("UPDATE users SET notes=" + dosql(notes) + " WHERE id = " + str(self.userId))
                messages.success(request, 'done')
                
            else: messages.error(request, 'toolong')
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---
        
        content = getTemplate(request, "s03/notes")

        self.selectedMenu = "notes"

        #---

        content.setValue("maxlength", 5000)

        #---

        notes = dbExecute("SELECT notes FROM users WHERE id = " + str(self.userId) + " LIMIT 1" )
        content.setValue("data_notes", notes)

        #---
        
        return self.display(content, request)
