# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "alliance.members"

        if self.AllianceId == None: return HttpResponseRedirect("/s03/alliance/")
        if not self.oAllianceRights["leader"] and not self.oAllianceRights["can_see_members_info"]: return HttpResponseRedirect("/s03/alliance/")

        self.invitation_success = ""

        cat = ToInt(request.GET.get("cat"), 1)
        if cat != 1 and cat != 2: cat = 1

        #
        # Process actions
        #
        action = request.GET.get("a", "").strip()
        self.username = request.POST.get("name", "").strip()

        if cat == 1:
            if self.oAllianceRights["leader"] and request.POST.get("submit", "") != "": self.SaveRanks()

            if self.oAllianceRights["can_kick_player"]:
                if action == "kick":
                    self.username = request.GET.get("name").strip()
                    oConnExecute("SELECT sp_alliance_kick_member("+str(self.userId)+","+dosql(self.username)+")")
        
        if cat == 2 and self.username != "":
            if self.oAllianceRights["can_invite_player"]:

                oRs = oConnExecute("SELECT sp_alliance_invite(" + str(self.userId) + "," + dosql(self.username) + ")")
                if oRs[0] == 0:
                    self.invitation_success = "ok"
                    self.username = ""
                elif oRs[0] == 1:
                    self.invitation_success = "norights"
                elif oRs[0] == 2:
                    self.invitation_success = "unknown"
                elif oRs[0] == 3:
                    self.invitation_success = "already_member"
                elif oRs[0] == 5:
                    self.invitation_success = "already_invited"
                elif oRs[0] == 6:
                    self.invitation_success = "impossible"

        return self.displayPage(cat)

    def displayMembers(self, content):
        col = ToInt(self.request.GET.get("col"), 1)
        if col < 1 or col > 7: col = 1

        reversed = False
        if col == 1:
            orderby = "upper(username)"
        elif col == 2:
            orderby = "score"
            reversed = True
        elif col == 3:
            orderby = "colonies"
            reversed = True
        elif col == 4:
            orderby = "credits"
            reversed = True
        elif col == 5:
            orderby = "lastactivity"
            reversed = True
        elif col == 6:
            orderby = "alliance_joined"
            reversed = True
        elif col == 7:
            orderby = "alliance_rank"
            reversed = False

        ParseR = False
        if self.request.GET.get("r", "") != "":
            reversed = not reversed
        else:
            ParseR = True

        if reversed: orderby = orderby + " DESC"
        orderby = orderby + ", upper(username)"

        # list ranks
        query = "SELECT rankid, label" + \
                " FROM alliances_ranks" + \
                " WHERE enabled AND allianceid=" + str(self.AllianceId) + \
                " ORDER BY rankid"
        oRss = oConnExecuteAll(query)
        
        list = []
        content.setValue("ranks", list)
        
        for oRs in oRss:
            
            item = {}
            list.append(item)
            
            item["rank_id"] = oRs[0]
            item["rank_label"] = oRs[1]

        # list members
        query = "SELECT username, CASE WHEN id="+str(self.userId)+" OR score_visibility >=1 THEN score ELSE 0 END AS score, int4((SELECT count(1) FROM nav_planet WHERE ownerid=users.id)) AS colonies," + \
                " date_part('epoch', now()-lastactivity) / 3600, alliance_joined, alliance_rank, privilege, score-previous_score AS score_delta, id," + \
                " 0, credits, score_visibility, orientation, COALESCE(date_part('epoch', leave_alliance_datetime-now()), 0)" + \
                " FROM users" + \
                " WHERE alliance_id=" + str(self.AllianceId) + \
                " ORDER BY " + orderby
        oRss = oConnExecuteAll(query)

        if self.oAllianceRights["can_kick_player"]:
            content.Parse("recruit")
        else:
            content.Parse("viewonly")

        if ParseR: content.Parse("r" + str(col))
        content.setValue("col", col)

        totalColonies = 0
        totalCredits = 0
        totalScore = 0
        totalScoreDelta = 0
        i = 1
        list = []
        content.setValue("players", list)
        for oRs in oRss:
            totalColonies = totalColonies + oRs[2]
            totalCredits = totalCredits + oRs[10]

            item = {}
            list.append(item)
            
            item["place"] = i
            item["name"] = oRs[0]
            item["score"] = oRs[1]
            item["score_delta"] = oRs[7]
            item["stat_colonies"] = oRs[2]
            item["hours_delay"] = int(oRs[3])
            item["days_delay"] = int(oRs[3] / 24)
            item["joined"] = oRs[4]
            item["rank"] = oRs[5]
            item["id"] = oRs[8]

            item["orientation" + str(oRs[12])] = True

            if oRs[5] > self.AllianceRank and self.oAllianceRights["can_kick_player"]:
                item["kick_price"] = oRs[9]
            else:
                item["kick_price"] = 0

            item["credits"] = oRs[10]

            if oRs[10] < 0: item["lowcredits"] = True

            if oRs[11] >= 1 or oRs[8] == self.userId:
                totalScore = totalScore + oRs[1]
                totalScoreDelta = totalScoreDelta + oRs[7]

                if oRs[7] > 0: item["score_plus"] = True
                if oRs[7] < 0: item["score_minus"] = True
                item["scoreshown"] = True
            else:
                item["score_na"] = True

            if oRs[6] == -1:
                item["banned"] = True
            elif oRs[6] == -2:
                item["onholidays"] = True
            #less than 15mins ? = 1/4 h
            elif oRs[3] < 0.25:
                item["online"] = True
            elif oRs[3] < 1:
                item["less1h"] = True
            elif oRs[3] < 1*24:
                item["hours"] = True
            elif oRs[3] < 7*24:
                item["days"] = True
            elif oRs[3] <= 14*24:
                item["1weekplus"] = True
            elif oRs[3] > 14*24:
                item["2weeksplus"] = True

            if self.oAllianceRights["leader"]:
                if oRs[5] > self.AllianceRank or oRs[8] == self.userId:
                    item["manage"] = True
                else:
                    item["cant_manage"] = True

            if oRs[13] > 0:
                item["leaving_time"] = oRs[13]
                item["leaving"] = True
            elif oRs[13] == 0:
                if self.oAllianceRights["can_kick_player"]:
                    if oRs[5] > self.AllianceRank:
                        item["kick"] = True
                    else:
                        item["cant_kick"] = True

            i = i + 1

        content.setValue("total_colonies", totalColonies)
        content.setValue("total_credits", totalCredits)
        content.setValue("total_score", totalScore)
        content.setValue("total_score_delta", totalScoreDelta)

        if totalScore != 0:
            if totalScoreDelta > 0: content.Parse("total_plus")
            if totalScoreDelta < 0: content.Parse("total_minus")
            content.Parse("score")
        else:
            content.Parse("score_na")

        content.Parse("members")

    def displayInvitations(self, content):

        if self.oAllianceRights["can_invite_player"]:
            query = "SELECT recruit.username, created, recruiters.username, declined" + \
                    " FROM alliances_invitations" + \
                    "        INNER JOIN users AS recruit ON recruit.id = alliances_invitations.userid" + \
                    "        LEFT JOIN users AS recruiters ON recruiters.id = alliances_invitations.recruiterid" + \
                    " WHERE allianceid=" + str(self.AllianceId) + \
                    " ORDER BY created DESC"

            oRss = oConnExecuteAll(query)

            i = 0
            list = []
            content.setValue("invits", list)
            for oRs in oRss:
                item = {}
                list.append(item)
                
                item["name"] = oRs[0]
                item["date"] = oRs[1]
                item["recruiter"] = oRs[2]

                if oRs[3]: item["declined"] = True
                else: item["waiting"] = True

                i = i + 1

            if i == 0: content.Parse("noinvitations")

            if self.invitation_success != "":
                content.Parse(self.invitation_success)
                content.Parse("message")

            content.setValue("player", self.username)

        content.Parse("invitations")

    #
    # Load template and display the right page
    #
    def displayPage(self, cat):

        content = getTemplate(self.request, "s03/alliance-members")

        content.setValue("cat", cat)

        if cat == 1:
            self.displayMembers(content)
        elif cat == 2:
            self.displayInvitations(content)

        content.Parse("cat" + str(cat) + "_selected")
        
        if self.oAllianceRights["can_invite_player"]:
            content.Parse("cat1")
            content.Parse("cat2")
            content.Parse("nav")

        return self.display(content)

    def SaveRanks(self):
        # retrieve alliance members# id and assign new rank
        query = "SELECT id" + \
                " FROM users" + \
                " WHERE alliance_id=" + str(self.AllianceId)
        oRss = oConnExecuteAll(query)

        for oRs in oRss:
            query = " UPDATE users SET" + \
                    " alliance_rank=" + str(ToInt(self.request.POST.get("player" + str(oRs[0])), 100)) + \
                    " WHERE id=" + str(oRs[0]) + " AND alliance_id=" + str(self.AllianceId) + " AND (alliance_rank > 0 OR id=" + str(self.userId) + ")"
            oConnDoQuery(query)

        # if leader demotes himself
        if ToInt(self.request.POST.get("player" + str(self.userId)), 100) > 0: return HttpResponseRedirect("/s03/alliance/")
