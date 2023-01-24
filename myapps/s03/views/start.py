# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from myapps.s03.lib.exile import *
from myapps.s03.lib.template import *
from myapps.s03.lib.accounts import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        if not registration["enabled"] or (registration["until"] != None and timezone.now() > registration["until"]):
            content = GetTemplate(self.request, "s03/start-closed")
            return render(self.request, content.template, content.data)

        result = 0

        self.UserId = int(request.session.get("user", 0))
        galaxy = int(request.POST.get("galaxy", 0))
        if galaxy == None: galaxy = 0

        if not self.UserId or self.UserId == 0:
            return HttpResponseRedirect("/")

        # check if it is the first login of the player
        rs = oConnExecute("SELECT login FROM users WHERE resets=0 AND id=" + str(self.UserId))
        if not rs:
            return HttpResponseRedirect("/")

        userName = rs[0]
        if not userName: userName = request.user.username

        newName = request.POST.get('name', '')
        if newName != "":
            # try to rename user and catch any error
            try:
                if isValidName(newName):
                    oConnDoQuery("UPDATE users SET login=" + dosql(newName) + " WHERE id=" + str(self.UserId))
                    userName = newName
                else:
                    result = 11
            except:
                result = 10

        if result == 0:
            orientation = int(request.POST.get("orientation", 0))
            allowed = False

            for i in allowedOrientations:
                if i == orientation:
                    allowed = True
                    break

            if allowed:
                oConnDoQuery("UPDATE users SET orientation=" + str(orientation) + " WHERE id=" + str(self.UserId))

                rs = oConnExecute("SELECT sp_reset_account(" + str(self.UserId) + "," + str(galaxy) + ")")
                result = rs[0]

                if result == 0:
    
                    if orientation == 1:    # merchant
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",10,1)")
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",11,1)")
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",12,1)")
    
                    elif orientation == 2:    # military
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",20,1)")
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",21,1)")
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",22,1)")
    
                    elif orientation == 3:    # scientist
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",30,1)")
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",31,1)")
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",32,1)")
    
                    elif orientation == 4:    # war lord
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",40,1)")
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",12,1)")
                        oConnDoQuery("INSERT INTO researches(userid, researchid, level) VALUES(" + str(self.UserId) + ",32,1)")
    
                    oConnExecute("SELECT sp_update_researches(" + str(self.UserId) + ")")
    
                    return HttpResponseRedirect("/s03/overview/")

        # display start page
        content = GetTemplate(self.request, "s03/start")
        content.AssignValue("login", userName)

        for i in allowedOrientations:
            content.Parse("orientation_" + str(i))

        rss = oConnExecuteAll("SELECT id, recommended FROM sp_get_galaxy_info(" + str(self.UserId) + ")")

        list = []
        content.AssignValue("galaxies", list)
        for rs in rss:
            item = {}
            list.append(item)
            item["id"] = rs[0]
            item["recommendation"] = rs[1]

        if result != 0:
            content.Parse("error_" + str(result))

        return render(self.request, content.template, content.data)
