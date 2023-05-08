# -*- coding: utf-8 -*-

from myapps.s03.views._utils import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        action = request.POST.get("unlock", "")
        
        if action != "":
            dbQuery("SELECT sp_stop_holidays(" + str(self.userId) + ")")
            return HttpResponseRedirect("/s03/overview/")
        
        return HttpResponseRedirect('/s03/holidays/')
        
    def get(self, request, *args, **kwargs):

        tpl = getTemplate(request, 's03/holidays')

        query = "SELECT username," + \
                " (SELECT int4(date_part('epoch', min_end_time-now())) FROM users_holidays WHERE userid=id) AS min_time," + \
                " (SELECT int4(date_part('epoch', end_time-now())) FROM users_holidays WHERE userid=id) AS remaining_time" + \
                " FROM users WHERE privilege=-2 AND id=" + str(self.userId)
        user = dbRow(query)
        
        if user == None: return HttpResponseRedirect("/")
        if user['remaining_time'] <= 0: return HttpResponseRedirect("/s03/overview/")
        
        tpl.setValue('user', user)
        
        return render(request, tpl.template, tpl.data)
