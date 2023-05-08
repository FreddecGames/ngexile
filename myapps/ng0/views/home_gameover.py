# -*- coding: utf-8 -*-

from myapps.ng0.views._base import *

class View(BaseView):

    def pre_dispatch(self, request, *args, **kwargs):
        
        #---
        
        result = dbExecute("SELECT int4(count(1)) FROM nav_planet WHERE ownerid=" + str(self.userId))
        if result == None: return HttpResponseRedirect("/")        

    def post(self, request, *args, **kwargs):

        action = request.POST.get("action")

        #---

        if action == "retry":
            
            username = request.POST.get("name", "")
            if not isValidName(username):
                messages.error(request, 'name_invalid')
                return HttpResponseRedirect('/ng0/game-over/')
                
            try:
                dbQuery("UPDATE users SET alliance_id=NULL, username=" + dosql(username) + " WHERE id=" + str(self.userId))
            except:
                messages.error(request, 'name_already_used')
                return HttpResponseRedirect('/ng0/game-over/')

            result = dbExecute("SELECT sp_reset_account(" + str(self.userId) + "," + str(ToInt(request.POST.get("galaxy"), 1)) + ")")
            if result == 0:
                return HttpResponseRedirect("/ng0/overview/")

            messages.error(request, 'error_' + result)
            return HttpResponseRedirect('/ng0/game-over/')

        #---
        
        elif action == "abandon":
        
            dbQuery("UPDATE users SET deletion_date=now()/*+INTERVAL '2 days'*/ WHERE id=" + str(self.userId))
            return HttpResponseRedirect("/")
        
        #---
        
        return HttpResponseRedirect('/ng0/game-over/')
        
    def get(self, request, *args, **kwargs):

        tpl = getTemplate(request, 'ng0/game-over')
        
        #---
        
        query = "SELECT username, resets, credits_bankruptcy FROM users WHERE id=" + str(self.userId)
        profile = dbRow(query)
        tpl.setValue("profile", profile)

        #---
        
        if profile['resets'] == 0: return HttpResponseRedirect("/ng0/start/")

        #---

        galaxies = dbRows('SELECT id, recommended FROM sp_get_galaxy_info(' + str(self.userId) + ')')
        tpl.setValue('galaxies', galaxies)

        #---

        return render(request, tpl.template, tpl.data)
