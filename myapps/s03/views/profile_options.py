from .base import *


class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "profile"

        if request.GET.get("frame") == "1":
            oConnDoQuery("UPDATE users SET inframe=True WHERE id="+ str(self.UserId))

        holidays_breaktime = 7*24*60*60 # time before being able to set the holidays again

        self.changes_status = ""
        self.showSubmit = True

        avatar = request.POST.get("avatar", "").strip()
        description = request.POST.get("description", "").strip()

        timers_enabled = ToInt(request.POST.get("timers_enabled"), 0)
        if timers_enabled == 1: timers_enabled = True
        else: timers_enabled = False

        display_alliance_planet_name = ToInt(request.POST.get("display_alliance_planet_name"), 0)
        if display_alliance_planet_name == 1: display_alliance_planet_name = True
        else: display_alliance_planet_name = False
        
        score_visibility = ToInt(request.POST.get("score_visibility"), 0)
        if score_visibility < 0 or score_visibility > 2: score_visibility = 0

        skin = ToInt(request.POST.get("skin"), 0)

        deletingaccount = request.POST.get("deleting")
        deleteaccount = request.POST.get("delete")

        autosignature = request.POST.get("autosignature")

        self.optionCat = ToInt(request.GET.get("cat"), 1)

        DoRedirect = False

        if self.optionCat < 1 or self.optionCat > 6:
            self.optionCat = 1

        if request.POST.get("submit", "") != "":

            self.changes_status = "done"
            query = ""

            if avatar != "" and not isValidURL(avatar):
                #avatar is invalid
                self.changes_status = "check_avatar"
            else:
                # save updated information
                query = "UPDATE users SET" + \
                        " avatar_url=" + dosql(avatar) + ", description=" + dosql(description) + \
                        " WHERE id=" + str(self.UserId)

            query = "UPDATE users SET" + \
                    " timers_enabled=" + str(timers_enabled) + \
                    " ,display_alliance_planet_name=" + str(display_alliance_planet_name) + \
                    " ,score_visibility=" + str(score_visibility)

            if skin == 0:
                skin = "s_default"
            else:
                skin = "s_transparent"

            query = query + ", skin=" + dosql(skin)

            if deletingaccount and not deleteaccount:
                query = query + ", deletion_date=NULL"

            if not deletingaccount and deleteaccount:
                query = query + ", deletion_date=now() + INTERVAL '2 days'"

            query = query + " WHERE id=" + str(self.UserId)

            if query != "": oConnDoQuery(query)
            DoRedirect = True

        if DoRedirect:
            return HttpResponseRedirect("/s03/profile-options/")
        else:
            return self.displayPage()

    def display_general(self, content):

        query = "SELECT avatar_url, regdate, users.description, 0," + \
                " alliance_id, a.tag, a.name, r.label" + \
                " FROM users" + \
                " LEFT JOIN alliances AS a ON (users.alliance_id = a.id)" + \
                " LEFT JOIN alliances_ranks AS r ON (users.alliance_id = r.allianceid AND users.alliance_rank = r.rankid) " + \
                " WHERE users.id = "+str(self.UserId)
        oRs = oConnExecute(query)

        content.AssignValue("regdate", oRs[1])
        content.AssignValue("description", oRs[2])
        content.AssignValue("ip", self.request.META.get("remote_addr"))

        if oRs[0] == None or oRs[0] == "":
            content.Parse("noavatar")
        else:
            content.AssignValue("avatar_url", oRs[0])
            content.Parse("avatar")

        if oRs[4]:
            content.AssignValue("alliancename", oRs[6])
            content.AssignValue("alliancetag", oRs[5])
            content.AssignValue("rank_label", oRs[7])

            content.Parse("alliance")
        else:
            content.Parse("noalliance")

        content.Parse("general")

    def display_options(self, content):

        oRs = oConnExecute("SELECT int4(date_part('epoch', deletion_date-now())), timers_enabled, display_alliance_planet_name, email, score_visibility, skin FROM users WHERE id="+str(self.UserId))

        if oRs[0] == None:
            content.Parse("delete_account")
        else:
            content.AssignValue("remainingtime", oRs[0])
            content.Parse("account_deleting")

        if oRs[1]: content.Parse("timers_enabled")
        if oRs[2]: content.Parse("display_alliance_planet_name")
        content.Parse("score_visibility_" + str(oRs[4]))

        content.Parse("skin_" + str(oRs[5]))

        content.AssignValue("email", str(oRs[3]))

        content.Parse("options")

    def display_holidays(self, content):

        # check if holidays will be activated soon
        oRs = oConnExecute("SELECT int4(date_part('epoch', start_time-now())) FROM users_holidays WHERE userid="+str(self.UserId))

        if oRs:
            remainingtime = oRs[0]
        else:
            remainingtime = 0

        if remainingtime > 0:
            content.AssignValue("remaining_time", remainingtime)
            content.Parse("start_in")
            self.showSubmit = False
        else:

            # holidays can be activated only if never took any holidays or it was at least 7 days ago
            oRs = oConnExecute("SELECT int4(date_part('epoch', now()-last_holidays)) FROM users WHERE id="+str(self.UserId))

            if (oRs[0]) and oRs[0] < holidays_breaktime:
                content.AssignValue("remaining_time", holidays_breaktime-oRs[0])
                content.Parse("cant_enable")
                self.showSubmit = False
            else:
                content.Parse("can_enable")

        content.Parse("holidays")

    def display_reports(self, content):

        oRss = oConnExecuteAll("SELECT type*100+subtype FROM users_reports WHERE userid="+str(self.UserId))
        for oRs in oRss:
            content.Parse("c"+str(oRs[0]))

        content.Parse("reports")

    def display_mail(self, content):

        oRs = oConnExecute("SELECT autosignature FROM users WHERE id="+str(self.UserId))
        if oRs:
            content.AssignValue("autosignature", oRs[0])
        else:
            content.AssignValue("autosignature", "")

        content.Parse("mail")

    def display_signature(self, content):

        content.Parse("signature")
        self.showSubmit = False

    def displayPage(self):
        content = GetTemplate(self.request, "profile-options")

        content.AssignValue("name", self.oPlayerInfo["username"])

        self.display_options(content)
        self.display_general(content)

        if self.changes_status != "":
            content.Parse(self.changes_status)
            content.Parse("changes")

        content.Parse("cat"+str(self.optionCat)+"_selected")
        content.Parse("cat1")
        content.Parse("cat2")
        content.Parse("cat5")
        content.Parse("cat6")
        content.Parse("nav")

        if self.showSubmit: content.Parse("submit")

        return self.Display(content)
