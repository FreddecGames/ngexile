# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
    
        name = request.POST.get('alliancename', '').strip()
        if not isValidAllianceName(name):
            messages.error(request, 'name_invalid')
            return HttpResponseRedirect('/s03/alliance-create/')
        
        #---

        tag = request.POST.get('alliancetag', '').strip()
        if not isValidAllianceTag(tag):
            messages.error(request, 'tag_invalid')
            return HttpResponseRedirect('/s03/alliance-create/')
        
        #---
        
        result = dbExecute("SELECT sp_create_alliance(" + str(self.userId) + "," + dosql(name) + "," + dosql(tag) + ", '')")
        if result >= -1:
            return HttpResponseRedirect("/s03/alliance/")
            
        if result == -2: messages.error(request, 'name_already_used')
        if result == -3: messages.error(request, 'tag_already_used')

        return HttpResponseRedirect('/s03/alliance-create/')

    def get(self, request, *args, **kwargs):

        tpl = getTemplate(self.request, "s03/alliance-create")

        self.selectedMenu = "noalliance.create"

        tpl.setValue("can_join_alliance", self.profile["can_join_alliance"])

        return self.display(tpl)
