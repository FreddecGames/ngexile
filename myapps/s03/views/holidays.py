# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from myapps.s03.lib.exile import *
from myapps.s03.lib.template import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.UserId = ToInt(self.request.session.get("user"), "")

        if self.UserId == "":
            return HttpResponseRedirect("/")

        content = GetTemplate(self.request, "s03/holidays")

        # retrieve remaining time
        query = "SELECT username," + \
                " (SELECT int4(date_part('epoch', min_end_time-now())) FROM users_holidays WHERE userid=id)," + \
                " (SELECT int4(date_part('epoch', end_time-now())) FROM users_holidays WHERE userid=id)" + \
                " FROM users WHERE privilege=-2 AND id=" + str(self.UserId)

        oRs = oConnExecute(query)
        
        if oRs == None:
            return HttpResponseRedirect("/")

        # check to unlock holidays mode
        action = request.POST.get("unlock", "")

        if action != "" and oRs[1] < 0:
            oConnExecute("SELECT sp_stop_holidays("+str(self.UserId)+")")
            return HttpResponseRedirect("/s03/overview/")

        # if remaining time is negative, return to overview page
        if oRs[2] <= 0:
            return HttpResponseRedirect("/s03/overview/")

        content.AssignValue("login", oRs[0])
        content.AssignValue("remaining_time", oRs[2])

        # only allow to unlock the account after 2 days of holidays
        if oRs[1] < 0:
            content.Parse("unlock")
        else:
            content.AssignValue("remaining_time_before_unlock", oRs[1])
            content.Parse("cant_unlock")

        return render(self.request, content.template, content.data)
