# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .exile import *
from .template import *
from .accounts import *

class View(ExileMixin, View):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        reset_error = 0

        self.UserId = ToInt(self.request.session.get("user"), "")

        if self.UserId == "":
            return HttpResponseRedirect("/s03/")

        # check that the player has no more planets
        oRs = oConnExecute("SELECT int4(count(1)) FROM nav_planet WHERE ownerid=" + str(self.UserId))
        if oRs == None:
            return HttpResponseRedirect("/s03/")

        planets = oRs[0]

        # retreive player username and number of resets

        query = "SELECT username, resets, credits_bankruptcy, int4(score_research) FROM users WHERE id=" + str(self.UserId)
        oRs = oConnExecute(query)

        username = oRs[0]
        resets = oRs[1]
        bankruptcy = oRs[2]
        research_done = oRs[3]

        # still have planets
        if planets > 0 and bankruptcy > 0:
            return HttpResponseRedirect("/s03/")

        if resets == 0:
            return HttpResponseRedirect("/s03/start/")

        changeNameError = ""

        if allowedRetry:
            action = request.POST.get("action")

            if action == "retry":
                # check if user wants to change name
                if request.POST.get("username") != username:

                    # check that the username is correct
                    if not isValidName(request.POST.get("username")):
                        changeNameError = "check_username"
                    else:
                        # try to rename user and catch any error
                        oConnDoQuery("UPDATE users SET alliance_id=NULL WHERE id=" + str(self.UserId))

                        oConnDoQuery("UPDATE users SET username=" + dosql(request.POST.get("username")) + " WHERE id=" + str(self.UserId))

                        if err.Number != 0:
                            changeNameError = "username_exists"
                        else:
                            # update the commander name
                            oConnDoQuery("UPDATE commanders SET name=" + dosql(request.POST.get("username")) + " WHERE name=" + dosql(username) + " AND ownerid=" + str(self.UserId))

                if changeNameError == "":
                    oRs = oConnExecute("SELECT sp_reset_account(" + str(self.UserId) + "," + str(ToInt(request.POST.get("galaxy"), 1)) + ")")
                    if oRs[0] == 0:
                        return HttpResponseRedirect("/s03/overview/")

                    else:
                        reset_error = oRs[0]

            elif action == "abandon":
                oConnDoQuery("UPDATE users SET deletion_date=now()/*+INTERVAL '2 days'*/ WHERE id=" + str(self.UserId))
                return HttpResponseRedirect("/s03/")

        # display Game Over page
        content = GetTemplate(self.request, "game-over")
        content.AssignValue("username", username)

        if changeNameError != "": action = "continue"

        if action == "continue":
            oRss = oConnExecuteAll("SELECT id, recommended FROM sp_get_galaxy_info(" + str(self.UserId) + ")")

            list = []
            for oRs in oRss:
                item = {}
                list.append(item)
                
                item["id"] = oRs[0]
                item["recommendation"] = oRs[1]

            content.AssignValue("galaxies", list)

            if changeNameError != "":
                content.Parse(changeNameError)
                content.Parse("error")

            content.Parse("changename")
        else:
            if allowedRetry: content.Parse("retry")
            content.Parse("choice")

            if bankruptcy > 0:
                content.Parse("gameover")
            else:
                content.Parse("bankrupt")

        if reset_error != 0:
            if reset_error == 4:
                content.Parse("no_free_planet")
            else:
                content.AssignValue("userid", self.UserId)
                content.AssignValue("reset_error", reset_error)
                content.Parse("reset_error")

        return render(self.request, content.template, content.data)
