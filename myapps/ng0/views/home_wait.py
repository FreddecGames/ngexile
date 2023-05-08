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
        
        action = request.POST.get('action', '')
        if action == 'unlock':
            dbQuery('UPDATE users SET privilege=0 WHERE id=' + str(self.userId))
            return HttpResponseRedirect('/ng0/overview/')
        
        return HttpResponseRedirect('/ng0/wait/')
        
    def get(self, request, *args, **kwargs):

        tpl = getTemplate(request, 'ng0/wait')

        profile = dbRow('SELECT username FROM users WHERE id=' + str(self.userId))
        tpl.setValue('profile', profile)

        return render(request, tpl.template, tpl.data)
