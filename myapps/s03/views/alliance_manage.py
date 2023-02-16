# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

from myapps.s03.views._utils import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "alliance.manage"

        if self.allianceId == None: return HttpResponseRedirect("/s03/alliance/")
        if not (self.allianceRights["leader"] or self.allianceRights["can_manage_description"] or self.allianceRights["can_manage_announce"]): return HttpResponseRedirect("/s03/alliance/")

        cat = ToInt(request.GET.get("cat", ""), 1)
        if cat < 1 or cat > 3: cat = 1

        if cat == 3 and not self.allianceRights["leader"]: cat=1
        if cat == 1 and not (self.allianceRights["leader"] or self.allianceRights["can_manage_description"]): cat=2
        if cat == 2 and not (self.allianceRights["leader"] or self.allianceRights["can_manage_announce"]): cat=1
        
        self.changes_status = ""
        
        if request.POST.get("submit", "") != "":
            if cat == 1: self.SaveGeneral()
            elif cat == 2: self.SaveMotD()
            elif cat == 3: self.SaveRanks()

        return self.displayOptions(cat)

    #
    # display alliance description page
    #
    def displayGeneral(self, content):

        # display alliance tag, name, description, creation date, number of members
        query = "SELECT id, tag, name, description, created, (SELECT count(*) FROM users WHERE alliance_id=alliances.id), logo_url," + \
                " max_members" + \
                " FROM alliances" + \
                " WHERE id=" + str(self.allianceId)

        oRs = oConnExecute(query)

        if oRs:
            content.setValue("tag", oRs[1])
            content.setValue("name", oRs[2])
            content.setValue("description", oRs[3])
            content.setValue("created", oRs[4])
            content.setValue("members", oRs[5])
            content.setValue("max_members", oRs[7])

            if oRs[6] != "":
                content.setValue("logo_url", oRs[6])
                content.Parse("logo")

        content.Parse("general")

    #
    # display alliance MotD (message of the day)
    #
    def displayMotD(self, content):

        # display alliance MotD (message of the day)
        query = "SELECT announce, defcon FROM alliances WHERE id=" + str(self.allianceId)
        oRs = oConnExecute(query)

        if oRs:
            content.setValue("announce", oRs[0])
            content.Parse("defcon_" + str(oRs[1]))

        content.Parse("motd")

    def displayRanks(self, content):
        # list ranks
        query = "SELECT rankid, label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, " + \
                " can_accept_money_requests, can_change_tax_rate, can_mail_alliance, is_default, members_displayed, can_manage_description, can_manage_announce, " + \
                " enabled, can_see_members_info, can_order_other_fleets, can_use_alliance_radars" + \
                " FROM alliances_ranks" + \
                " WHERE allianceid=" + str(self.allianceId) + \
                " ORDER BY rankid"
        oRss = dbRows(query)
        list = []
        for oRs in oRss:
            item = {}
            item["rank_id"] = oRs["rankid"]
            item["rank_label"] = oRs["label"]

            if oRs["leader"]: item["disabled"] = True

            if oRs["leader"] or oRs["enabled"]: item["checked_enabled"] = True

            if oRs["leader"] or oRs["is_default"] and not oRs["leader"]: item["checked_0"] = True

            if oRs["leader"] or oRs["can_invite_player"]: item["checked_1"] = True
            if oRs["leader"] or oRs["can_kick_player"]: item["checked_2"] = True

            if oRs["leader"] or oRs["can_create_nap"]: item["checked_3"] = True
            if oRs["leader"] or oRs["can_break_nap"]: item["checked_4"] = True

            if oRs["leader"] or oRs["can_ask_money"]: item["checked_5"] = True
            if oRs["leader"] or oRs["can_see_reports"]: item["checked_6"] = True

            if oRs["leader"] or oRs["can_accept_money_requests"]: item["checked_7"] = True
            if oRs["leader"] or oRs["can_change_tax_rate"]: item["checked_8"] = True

            if oRs["leader"] or oRs["can_mail_alliance"]: item["checked_9"] = True

            if oRs["leader"] or oRs["can_manage_description"]: item["checked_10"] = True
            if oRs["leader"] or oRs["can_manage_announce"]: item["checked_11"] = True

            if oRs["leader"] or oRs["can_see_members_info"]: item["checked_12"] = True

            if oRs["leader"] or oRs["members_displayed"]: item["checked_13"] = True

            if oRs["leader"] or oRs["can_order_other_fleets"]: item["checked_14"] = True
            if oRs["leader"] or oRs["can_use_alliance_radars"]: item["checked_15"] = True

            list.append(item)

        content.setValue("ranks", list)

    #
    # Load template and display the right page
    #
    def displayOptions(self, cat):

        content = getTemplate(self.request, "s03/alliance-manage")
        content.setValue("cat", cat)
        
        if cat == 1:
            self.displayGeneral(content)
        elif cat == 2:
            self.displayMotD(content)
        elif cat == 3:
            self.displayRanks(content)

        if self.changes_status != "":
            content.Parse(self.changes_status)
            content.Parse("error")

        content.Parse("cat"+str(cat)+"_selected")
        if self.allianceRights["leader"] or self.allianceRights["can_manage_description"]: content.Parse("cat1")
        if self.allianceRights["leader"] or self.allianceRights["can_manage_announce"]: content.Parse("cat2")
        if self.allianceRights["leader"]: content.Parse("cat3")
        content.Parse("nav")

        return self.display(content)

    def SaveGeneral(self):

        logo = self.request.POST.get("logo", "").strip()
        description = self.request.POST.get("description", "").strip()

        print(self.request.POST)

        if logo != "" and not isValidURL(logo):
            #logo is invalid
            self.changes_status = "check_logo"
        else:
            # save updated information
            oConnDoQuery("UPDATE alliances SET logo_url=" + dosql(logo) + ", description=" + dosql(description) + " WHERE id = " + str(self.allianceId))

            self.changes_status = "done"

    def SaveMotD(self):
        MotD = self.request.POST.get("motd").strip()
        defcon = ToInt(self.request.POST.get("defcon"), 5)

        # save updated information
        oConnDoQuery("UPDATE alliances SET defcon=" + str(defcon) + ", announce=" + dosql(MotD) + " WHERE id = " + str(self.allianceId))
        self.changes_status = "done"

    def SaveRanks(self):
    
        query = "SELECT rankid, leader" + \
            " FROM alliances_ranks" + \
            " WHERE allianceid=" + str(self.allianceId) + \
            " ORDER BY rankid"
        oRss = dbRows(query)
        for oRs in oRss:
            name = self.request.POST.get("n" + str(oRs['rankid'])).strip()
            if len(name) > 2:
                query = "UPDATE alliances_ranks SET" + \
                        " label=" + dosql(name) + \
                        ", is_default=NOT leader AND " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_0"), False)) + \
                        ", can_invite_player=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_1"), False)) + \
                        ", can_kick_player=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_2"), False)) + \
                        ", can_create_nap=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_3"), False)) + \
                        ", can_break_nap=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_4"), False)) + \
                        ", can_ask_money=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_5"), False)) + \
                        ", can_see_reports=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_6"), False)) + \
                        ", can_accept_money_requests=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_7"), False)) + \
                        ", can_change_tax_rate=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_8"), False)) + \
                        ", can_mail_alliance=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_9"), False)) + \
                        ", can_manage_description=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_10"), False)) + \
                        ", can_manage_announce=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_11"), False)) + \
                        ", can_see_members_info=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_12"), False)) + \
                        ", members_displayed=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_13"), False)) + \
                        ", can_order_other_fleets=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_14"), False)) + \
                        ", can_use_alliance_radars=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_15"), False)) + \
                        ", enabled=leader OR EXISTS(SELECT 1 FROM users WHERE alliance_id=" + str(self.allianceId) + " AND alliance_rank=" + str(oRs['rankid']) + " LIMIT 1) OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_enabled"), False)) + " OR " + str(ToBool(self.request.POST.get("c" + str(oRs['rankid']) + "_0"), False)) + \
                        " WHERE allianceid=" + str(self.allianceId) + " AND rankid=" + str(oRs['rankid'])

                connExecuteRetryNoRecords(query)
