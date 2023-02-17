# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "alliance.naps"

        self.invitation_success = ""
        self.break_success = ""
        self.nap_success = ""

        cat = ToInt(request.GET.get("cat"), 0)
        if cat < 1 or cat > 3: cat = 1

        if not self.allianceRights["can_create_nap"] and cat == 3: cat = 1
        if not (self.allianceRights["can_create_nap"] or self.allianceRights["can_break_nap"]) and cat != 1: cat = 1

        #
        # Process actions
        #

        # redirect the player to the alliance page if he is not part of an alliance
        if self.allianceId == None:
            return HttpResponseRedirect("/s03/alliance/")

        action = request.GET.get("a", "")
        targetalliancetag = request.GET.get("tag", "").strip()

        self.tag = ""
        self.hours = 24

        if action == "accept":
            oRs = oConnExecute("SELECT sp_alliance_nap_accept(" + str(self.userId) + "," + dosql(targetalliancetag) + ")")
            if oRs[0] == 0:
                self.nap_success = "ok"
            elif oRs[0] == 5:
                self.nap_success = "too_many"

        elif action == "decline":
            oConnExecute("SELECT sp_alliance_nap_decline(" + str(self.userId) + "," + dosql(targetalliancetag) + ")")
        elif action == "cancel":
            oConnExecute("SELECT sp_alliance_nap_cancel(" + str(self.userId) + "," + dosql(targetalliancetag) + ")")
        elif action == "sharelocs":
            oConnExecute("SELECT sp_alliance_nap_toggle_share_locs(" + str(self.userId) + "," + dosql(targetalliancetag) + ")")
        elif action == "shareradars":
            oConnExecute("SELECT sp_alliance_nap_toggle_share_radars(" + str(self.userId) + "," + dosql(targetalliancetag) + ")")
        elif action == "break":
            oRs = oConnExecute("SELECT sp_alliance_nap_break(" + str(self.userId) + "," + dosql(targetalliancetag) + ")")

            if oRs[0] == 0:
                self.break_success = "ok"
            elif oRs[0] == 1:
                self.break_success = "norights"
            elif oRs[0] == 2:
                self.break_success = "unknown"
            elif oRs[0] == 3:
                self.break_success = "nap_not_found"
            elif oRs[0] == 4:
                self.break_success = "not_enough_credits"

        elif action == "new":
            self.tag = request.POST.get("tag", "").strip()

            self.hours = ToInt(request.POST.get("hours"), 0)

            oRs = oConnExecute("SELECT sp_alliance_nap_request(" + str(self.userId) + "," + dosql(self.tag) + "," + str(self.hours) + ")")
            if oRs[0] == 0:
                self.invitation_success = "ok"
                self.tag = ""
                self.hours = 24
            elif oRs[0] == 1:
                self.invitation_success = "norights"
            elif oRs[0] == 2:
                self.invitation_success = "unknown"
            elif oRs[0] == 3:
                self.invitation_success = "already_naped"
            elif oRs[0] == 4:
                self.invitation_success = "request_waiting"
            elif oRs[0] == 6:
                self.invitation_success = "already_requested"

        return self.displayPage(cat)

    def displayNAPs(self, content):
        col = ToInt(self.request.GET.get("col"), 0)
        if col < 1 or col > 6: col = 1
        if col == 2: col = 1

        reversed = False
        if col == 1:
            orderby = "tag"
        elif col == 3:
            orderby = "created"
            reversed = True
        elif col == 4:
            orderby = "break_interval"
        elif col == 5:
            orderby = "share_locs"
        elif col == 6:
            orderby = "share_radars"

        if self.request.GET.get("r", "") != "":
            reversed = not reversed
        else:
            content.Parse("r" + str(col))
        content.setValue("col", col)
        
        if reversed: orderby = orderby + " DESC"
        orderby = orderby + ", tag"

        # List Non Aggression Pacts
        query = "SELECT n.allianceid2, tag, name, " + \
                " (SELECT COALESCE(sum(score)/1000, 0) AS score FROM users WHERE alliance_id=allianceid2), n.created, date_part('epoch', n.break_interval)::integer, date_part('epoch', break_on-now())::integer," + \
                " share_locs, share_radars" + \
                " FROM alliances_naps n" + \
                "    INNER JOIN alliances ON (allianceid2 = alliances.id)" + \
                " WHERE allianceid1=" + str(self.allianceId) + \
                " ORDER BY " + orderby
        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.setValue("naps", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["place"] = i+1
            item["tag"] = oRs[1]
            item["name"] = oRs[2]
            item["score"] = oRs[3]
            item["created"] = oRs[4]

            if oRs[6] == None:
                item["break_interval"] = oRs[5]
                item["time"] = True
            else:
                item["break_interval"] = oRs[6]
                item["countdown"] = True

            if oRs[7]:
                item["locs_shared"] = True
            else:
                item["locs_not_shared"] = True

            if self.allianceRights["can_create_nap"]:
                item["toggle_share_locs"] = True

            if oRs[8]:
                item["radars_shared"] = True
            else:
                item["radars_not_shared"] = True

            if self.allianceRights["can_create_nap"]:
                item["toggle_share_radars"] = True

            if self.allianceRights["can_break_nap"]:
                if oRs[6] == None:
                    item["break"] = True
                else:
                    item["broken"] = True

            i = i + 1

        if self.allianceRights["can_break_nap"] and (i > 0): content.Parse("break")

        if i == 0: content.Parse("nonaps")

        if self.break_success != "":
            content.Parse(self.break_success)
            content.Parse("message")

    def displayPropositions(self, content):

        # List NAPs that other alliances have offered
        query = "SELECT alliances.tag, alliances.name, alliances_naps_offers.created, recruiters.username, declined, date_part('epoch', break_interval)::integer" + \
                " FROM alliances_naps_offers" + \
                "            INNER JOIN alliances ON alliances.id = alliances_naps_offers.allianceid" + \
                "            LEFT JOIN users AS recruiters ON recruiters.id = alliances_naps_offers.recruiterid" + \
                " WHERE targetallianceid=" + str(self.allianceId) + " AND NOT declined" + \
                " ORDER BY created DESC"
        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.setValue("propositions", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["tag"] = oRs[0]
            item["name"] = oRs[1]
            item["date"] = oRs[2]
            item["recruiter"] = oRs[3]

            if oRs[4]: item["declined"] = True
            else: item["waiting"] = True

            item["break_interval"] = oRs[5]

            i = i + 1

        if i == 0: content.Parse("nopropositions")

        if self.nap_success != "":
            content.Parse(self.nap_success)
            content.Parse("message")

    def displayRequests(self, content):

        # List NAPs we proposed to other alliances
        query = "SELECT alliances.tag, alliances.name, alliances_naps_offers.created, recruiters.username, declined, date_part('epoch', break_interval)::integer" + \
                " FROM alliances_naps_offers" + \
                "            INNER JOIN alliances ON alliances.id = alliances_naps_offers.targetallianceid" + \
                "            LEFT JOIN users AS recruiters ON recruiters.id = alliances_naps_offers.recruiterid" + \
                " WHERE allianceid=" + str(self.allianceId) + \
                " ORDER BY created DESC"

        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.setValue("newnaps", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["tag"] = oRs[0]
            item["name"] = oRs[1]
            item["date"] = oRs[2]
            item["recruiter"] = oRs[3]

            if oRs[4]: item["declined"] = True
            else: item["waiting"] = True

            item["break_interval"] = oRs[5]

            i = i + 1

        if i == 0: content.Parse("norequests")

        if self.invitation_success != "":
            content.Parse(self.invitation_success)
            content.Parse("message")

        content.setValue("tag", self.tag)
        content.setValue("hours", self.hours)

    def displayPage(self, cat):
        content = getTemplate(self.request, "s03/alliance-naps")
        content.setValue("cat", cat)

        if cat == 1:
            self.displayNAPs(content)
        elif cat == 2:
            self.displayPropositions(content)
        elif cat == 3:
            self.displayRequests(content)

        content.Parse("cat" + str(cat) + "_selected")
        if self.allianceRights["can_create_nap"] or self.allianceRights["can_break_nap"]:

            query = "SELECT int4(count(*)) FROM alliances_naps_offers" + \
                    " WHERE targetallianceid=" + str(self.allianceId) + " AND NOT declined"
            oRs = oConnExecute(query)
            content.setValue("proposition_count", oRs[0])

            query = "SELECT int4(count(*)) FROM alliances_naps_offers" + \
                    " WHERE allianceid=" + str(self.allianceId) + " AND NOT declined"
            oRs = oConnExecute(query)
            content.setValue("request_count", oRs[0])

            content.Parse("cat1")
            content.Parse("cat2")
            if self.allianceRights["can_create_nap"]: content.Parse("cat3")
            content.Parse("nav")

        return self.display(content)
