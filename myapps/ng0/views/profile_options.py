from .base import *


class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "profile"

        holidays_breaktime = 7*24*60*60 # time before being able to set the holidays again

        self.changes_status = ""
        self.showSubmit = True

        avatar = request.POST.get("avatar", "").strip()
        description = request.POST.get("description", "").strip()
        
        score_visibility = toInt(request.POST.get("score_visibility"), 0)
        if score_visibility < 0 or score_visibility > 2: score_visibility = 0

        skin = toInt(request.POST.get("skin"), 0)

        deletingaccount = request.POST.get("deleting")
        deleteaccount = request.POST.get("delete")

        autosignature = request.POST.get("autosignature")

        self.optionCat = toInt(request.GET.get("cat"), 1)

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
                        " avatar_url=" + strSql(avatar) + ", description=" + strSql(description)

            query = query + ", score_visibility=" + str(score_visibility)

            if deletingaccount and not deleteaccount:
                query = query + ", deletion_date=NULL"

            if not deletingaccount and deleteaccount:
                query = query + ", deletion_date=now() + INTERVAL '2 days'"

            query = query + " WHERE id=" + str(self.profile['id'])
            
            if query != "": dbQuery(query)
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
                " WHERE users.id = "+str(self.profile['id'])
        oRs = oConnExecute(query)

        content.assignValue("regdate", oRs[1])
        content.assignValue("description", oRs[2])
        content.assignValue("ip", self.request.META.get("remote_addr"))

        if oRs[0] == None or oRs[0] == "":
            content.parse("noavatar")
        else:
            content.assignValue("avatar_url", oRs[0])
            content.parse("avatar")

        if oRs[4]:
            content.assignValue("alliancename", oRs[6])
            content.assignValue("alliancetag", oRs[5])
            content.assignValue("rank_label", oRs[7])

            content.parse("alliance")
        else:
            content.parse("noalliance")

        content.parse("general")

    def display_options(self, content):

        oRs = oConnExecute("SELECT int4(date_part('epoch', deletion_date-now())), timers_enabled, display_alliance_planet_name, email, score_visibility FROM users WHERE id="+str(self.profile['id']))

        if oRs[0] == None:
            content.parse("delete_account")
        else:
            content.assignValue("remainingtime", oRs[0])
            content.parse("account_deleting")

        content.parse("score_visibility_" + str(oRs[4]))

        content.assignValue("email", str(oRs[3]))

        content.parse("options")

    def display_holidays(self, content):

        # check if holidays will be activated soon
        oRs = oConnExecute("SELECT int4(date_part('epoch', start_time-now())) FROM users_holidays WHERE userid="+str(self.profile['id']))

        if oRs:
            remainingtime = oRs[0]
        else:
            remainingtime = 0

        if remainingtime > 0:
            content.assignValue("remaining_time", remainingtime)
            content.parse("start_in")
            self.showSubmit = False
        else:

            # holidays can be activated only if never took any holidays or it was at least 7 days ago
            oRs = oConnExecute("SELECT int4(date_part('epoch', now()-last_holidays)) FROM users WHERE id="+str(self.profile['id']))

            if (oRs[0]) and oRs[0] < holidays_breaktime:
                content.assignValue("remaining_time", holidays_breaktime-oRs[0])
                content.parse("cant_enable")
                self.showSubmit = False
            else:
                content.parse("can_enable")

        content.parse("holidays")

    def display_reports(self, content):

        oRss = oConnExecuteAll("SELECT type*100+subtype FROM users_reports WHERE userid="+str(self.profile['id']))
        for oRs in oRss:
            content.parse("c"+str(oRs[0]))

        content.parse("reports")

    def display_mail(self, content):

        oRs = oConnExecute("SELECT autosignature FROM users WHERE id="+str(self.profile['id']))
        if oRs:
            content.assignValue("autosignature", oRs[0])
        else:
            content.assignValue("autosignature", "")

        content.parse("mail")

    def display_signature(self, content):

        content.parse("signature")
        self.showSubmit = False

    def displayPage(self):
        content = getTemplateContext(self.request, "profile-options")

        content.assignValue("name", self.oPlayerInfo["username"])

        self.display_options(content)
        self.display_general(content)

        if self.changes_status != "":
            content.parse(self.changes_status)
            content.parse("changes")

        content.parse("cat"+str(self.optionCat)+"_selected")
        content.parse("cat1")
        content.parse("cat2")
        content.parse("cat5")
        content.parse("cat6")
        content.parse("nav")

        if self.showSubmit: content.parse("submit")

        return self.display(content)
