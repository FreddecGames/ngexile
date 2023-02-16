# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from myapps.s03.views._utils import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        reset_error = 0

        self.userId = ToInt(self.request.session.get("user"), "")

        if self.userId == "":
            return HttpResponseRedirect("/")

        # check that the player has no more planets
        oRs = oConnExecute("SELECT int4(count(1)) FROM nav_planet WHERE ownerid=" + str(self.userId))
        if oRs == None:
            return HttpResponseRedirect("/")

        planets = oRs[0]

        # retreive player username and number of resets

        query = "SELECT username, resets, credits_bankruptcy, int4(score_research) FROM users WHERE id=" + str(self.userId)
        oRs = oConnExecute(query)

        username = oRs[0]
        resets = oRs[1]
        bankruptcy = oRs[2]
        research_done = oRs[3]

        # still have planets
        if planets > 0 and bankruptcy > 0:
            return HttpResponseRedirect("/")

        if resets == 0:
            return HttpResponseRedirect("/s03/start/")

        changeNameError = ""

        action = request.POST.get("action")

        if action == "retry":
            # check if user wants to change name
            if request.POST.get("username") != username:

                # check that the login is not banned
                oRs = oConnExecute("SELECT 1 FROM banned_logins WHERE " + dosql(username) + " ~* login LIMIT 1;")
                if oRs == None:

                    # check that the username is correct
                    if not isValidName(request.POST.get("username")):
                        changeNameError = "check_username"
                    else:
                        # try to rename user and catch any error
                        oConnDoQuery("UPDATE users SET alliance_id=NULL WHERE id=" + str(self.userId))

                        oConnDoQuery("UPDATE users SET username=" + dosql(request.POST.get("username")) + " WHERE id=" + str(self.userId))

                        if err.Number != 0:
                            changeNameError = "username_exists"
                        else:
                            # update the commander name
                            oConnDoQuery("UPDATE commanders SET name=" + dosql(request.POST.get("login")) + " WHERE name=" + dosql(username) + " AND ownerid=" + str(self.userId))

            if changeNameError == "":
                oRs = oConnExecute("SELECT sp_reset_account(" + str(self.userId) + "," + str(ToInt(request.POST.get("galaxy"), 1)) + ")")
                if oRs[0] == 0:
                    return HttpResponseRedirect("/s03/overview/")

                else:
                    reset_error = oRs[0]

        elif action == "abandon":
            oConnDoQuery("UPDATE users SET deletion_date=now()/*+INTERVAL '2 days'*/ WHERE id=" + str(self.userId))
            return HttpResponseRedirect("/")

        # display Game Over page
        content = getTemplate(self.request, "s03/game-over")
        content.setValue("login", username)

        if changeNameError != "": action = "continue"

        if action == "continue":
            oRss = oConnExecuteAll("SELECT id, recommended FROM sp_get_galaxy_info(" + str(self.userId) + ")")

            list = []
            for oRs in oRss:
                item = {}
                list.append(item)
                
                item["id"] = oRs[0]
                item["recommendation"] = oRs[1]

            content.setValue("galaxies", list)

            if changeNameError != "":
                content.Parse(changeNameError)
                content.Parse("error")

            content.Parse("changename")
        else:
            content.Parse("retry")
            content.Parse("choice")

            if bankruptcy > 0:
                content.Parse("gameover")
            else:
                content.Parse("bankrupt")

        if reset_error != 0:
            if reset_error == 4:
                content.Parse("no_free_planet")
            else:
                content.setValue("userid", self.userId)
                content.setValue("reset_error", reset_error)
                content.Parse("reset_error")

        return render(self.request, content.template, content.data)
