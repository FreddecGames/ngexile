# -*- coding: utf-8 -*-

from myapps.s04.views._utils import *

class View(BaseView):

    ################################################################################

    def dispatch(self, request, *args, **kwargs):
        
        #---
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
            
        #---
        
        query = 'SELECT * FROM s04.vw_profiles' + \
                ' WHERE id=' + str(self.userId)
        self.profile = dbRow(query)

        if self.profile['status'] != 'new': return HttpResponseRedirect('/s04/')
        
        #---
        
        if (not registration) and (not request.user.is_superuser):
        
            tpl = getTemplate(request, 'home-closed')
            
            return render(request, tpl.template, tpl.data)
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')

        #---
        
        if action == 'start':

            name = request.POST.get('name', '').strip()
            if not isValidName(name):
                messages.error(request, gettext('Le nom saisi est invalide'))
                return HttpResponseRedirect(request.build_absolute_uri())

            try:
                dbQuery('UPDATE s04.profiles SET name=' + dosql(name) + ' WHERE id=' + str(self.userId))
            except:
                messages.error(request, gettext('Le nom saisi est déjà utilisé'))
                return HttpResponseRedirect(request.build_absolute_uri())

            result = dbExecute('SELECT sp_profile_reset(' + str(self.userId) + ')')
            if result != 0:
                if result == -1: messages.error(request, gettext('Utilisateur inconnu'))
                elif result == -2: messages.error(request, gettext('Plus de planète disponible'))
                else: messages.error(request, gettext('Erreur inconnue ' + result))
                return HttpResponseRedirect(request.build_absolute_uri())

            return HttpResponseRedirect('/s04/')

        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):

        #---

        tpl = getTemplate(request, 'home-start')

        #---
        
        return render(request, tpl.template, tpl.data)
