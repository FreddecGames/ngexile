from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "alliance"

        if self.AllianceId == None: return HttpResponseRedirect("/s03/alliance-view/")
        if not (self.oAllianceRights["leader"] or self.oAllianceRights["can_manage_description"] or self.oAllianceRights["can_manage_announce"]): return HttpResponseRedirect("/s03/alliance-view/")

        cat = ToInt(request.GET.get("cat", ""), 1)
        if cat < 1 or cat > 3: cat = 1

        if cat == 3 and not self.oAllianceRights["leader"]: cat=1
        if cat == 1 and not (self.oAllianceRights["leader"] or self.oAllianceRights["can_manage_description"]): cat=2
        if cat == 2 and not (self.oAllianceRights["leader"] or self.oAllianceRights["can_manage_announce"]): cat=1
        
        self.changes_status = ""

        if request.POST.get("submit", "") != "":
            self.SaveGeneral()
            self.SaveMotD()

        return self.displayOptions(cat)

    #
    # Display alliance description page
    #
    def displayGeneral(self, content):

        # Display alliance tag, name, description, creation date, number of members
        query = "SELECT id, tag, name, description, created, (SELECT count(*) FROM users WHERE alliance_id=alliances.id), logo_url," + \
                " max_members" + \
                " FROM alliances" + \
                " WHERE id=" + str(self.AllianceId)

        oRs = oConnExecute(query)

        if oRs:
            content.AssignValue("tag", oRs[1])
            content.AssignValue("name", oRs[2])
            content.AssignValue("description", oRs[3])
            content.AssignValue("created", oRs[4])
            content.AssignValue("members", oRs[5])
            content.AssignValue("max_members", oRs[7])

            if oRs[6] != "":
                content.AssignValue("logo_url", oRs[6])
                content.Parse("logo")

        content.Parse("general")

    #
    # Display alliance MotD (message of the day)
    #
    def displayMotD(self, content):

        # Display alliance MotD (message of the day)
        query = "SELECT announce, defcon FROM alliances WHERE id=" + str(self.AllianceId)
        oRs = oConnExecute(query)

        if oRs:
            content.AssignValue("announce", oRs[0])
            content.Parse("defcon_" + str(oRs[1]))

        content.Parse("motd")

    #
    # Load template and display the right page
    #
    def displayOptions(self, cat):

        content = GetTemplate(self.request, "alliance-manage")
        content.AssignValue("cat", cat)
        
        self.displayGeneral(content)
        self.displayMotD(content)

        if self.changes_status != "":
            content.Parse(self.changes_status)
            content.Parse("error")

        content.Parse("cat"+str(cat)+"_selected")
        if self.oAllianceRights["leader"] or self.oAllianceRights["can_manage_description"]: content.Parse("cat1")
        if self.oAllianceRights["leader"] or self.oAllianceRights["can_manage_announce"]: content.Parse("cat2")
        if self.oAllianceRights["leader"]: content.Parse("cat3")
        content.Parse("nav")

        return self.Display(content)

    def SaveGeneral(self):

        logo = self.request.POST.get("logo", "").strip()
        description = self.request.POST.get("description", "").strip()
        
        print(self.request.POST)
        
        if logo != "" and not isValidURL(logo):
            #logo is invalid
            self.changes_status = "check_logo"
        else:
            # save updated information
            oConnDoQuery("UPDATE alliances SET logo_url=" + dosql(logo) + ", description=" + dosql(description) + " WHERE id = " + str(self.AllianceId))

            self.changes_status = "done"

    def SaveMotD(self):
        MotD = self.request.POST.get("motd").strip()
        defcon = ToInt(self.request.POST.get("defcon"), 5)

        # save updated information
        oConnDoQuery("UPDATE alliances SET defcon=" + str(defcon) + ", announce=" + dosql(MotD) + " WHERE id = " + str(self.AllianceId))
        self.changes_status = "done"

    def SaveRanks(self):

        # list ranks
        query = "SELECT rankid, leader" + \
                " FROM alliances_ranks" + \
                " WHERE allianceid=" + str(self.AllianceId) + \
                " ORDER BY rankid"
        oRss = oConnExecuteAll(query)
        for oRs in oRss:
            name = self.request.POST.get("n" + str(oRs[0]), "").strip()
            if len(name) > 2:
                query = "UPDATE alliances_ranks SET" + \
                        " label=" + dosql(name) + \
                        ", is_default=NOT leader AND " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_0"), False)) + \
                        ", can_invite_player=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_1"), False)) + \
                        ", can_kick_player=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_2"), False)) + \
                        ", can_create_nap=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_3"), False)) + \
                        ", can_break_nap=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_4"), False)) + \
                        ", can_ask_money=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_5"), False)) + \
                        ", can_see_reports=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_6"), False)) + \
                        ", can_accept_money_requests=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_7"), False)) + \
                        ", can_change_tax_rate=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_8"), False)) + \
                        ", can_mail_alliance=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_9"), False)) + \
                        ", can_manage_description=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_10"), False)) + \
                        ", can_manage_announce=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_11"), False)) + \
                        ", can_see_members_info=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_12"), False)) + \
                        ", members_displayed=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_13"), False)) + \
                        ", can_order_other_fleets=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_14"), False)) + \
                        ", can_use_alliance_radars=leader OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_15"), False)) + \
                        ", enabled=leader OR EXISTS(SELECT 1 FROM users WHERE alliance_id=" + str(self.AllianceId) + " AND alliance_rank=" + str(oRs[0])+ " LIMIT 1) OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_enabled"), False)) + " OR " + str(ToBool(self.request.POST.get("c" + str(oRs[0]) + "_0"), False)) + \
                        " WHERE allianceid=" + str(self.AllianceId) + " AND rankid=" + str(oRs[0])

                oConnDoQuery(query)
