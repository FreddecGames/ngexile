# -*- coding: utf-8 -*-

from ._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "allianceno."

        tag = request.GET.get("tag")

        if tag and tag != "":
            return self.DisplayAlliance(tag)
        else:
            if self.AllianceId == None:
                return HttpResponseRedirect("/s03/alliance-invitations/")
            else:
                return self.DisplayAlliance(None)

    def DisplayAlliance(self, alliance_tag):

        content = GetTemplate(self.request, "alliance")

        self.selected_menu = "alliance.overview"

        query = "SELECT id, name, tag, description, created, (SELECT count(*) FROM users WHERE alliance_id=alliances.id)," + \
                " logo_url, website_url, max_members" + \
                " FROM alliances"

        if alliance_tag == None:
            query = query + " WHERE id=" + str(self.AllianceId) + " LIMIT 1"
        else:
            query = query + " WHERE tag=upper(" + dosql(alliance_tag) + ") LIMIT 1"
            self.selected_menu = "ranking"

        oRs = oConnExecute(query)

        if oRs:
            alliance_id = oRs[0]
            content.AssignValue("name", oRs[1])
            content.AssignValue("tag", oRs[2])
            content.AssignValue("description", oRs[3])

            created = oRs[4]
            content.AssignValue("created", created)
            content.AssignValue("members", oRs[5])
            content.AssignValue("max_members", oRs[8])

            if oRs[6] and oRs[6] != "":
                content.AssignValue("logo_url", oRs[6])
                content.Parse("logo")

            #
            # Display Non Aggression Pacts (NAP)
            #
            NAPcount = 0

            query = "SELECT allianceid1, tag, name" + \
                    " FROM alliances_naps INNER JOIN alliances ON (alliances_naps.allianceid1=alliances.id)" + \
                    " WHERE allianceid2=" + str(alliance_id)
            oRss = oConnExecuteAll(query)

            if oRss:
                list = []
                for oRs in oRss:
                    item = {}
                    item["naptag"] = oRs[1]
                    item["napname"] = oRs[2]
                    list.append(item)
                    NAPcount = NAPcount + 1
                content.AssignValue("naps", list)

            if NAPcount == 0:
                content.Parse("nonaps")

            #
            # Display WARs
            #
            WARcount = 0

            query = "SELECT w.created, alliances.id, alliances.tag, alliances.name"+ \
                " FROM alliances_wars w" + \
                "    INNER JOIN alliances ON (allianceid2 = alliances.id)" + \
                " WHERE allianceid1=" + str(alliance_id) + \
                " UNION " + \
                "SELECT w.created, alliances.id, alliances.tag, alliances.name"+ \
                " FROM alliances_wars w" + \
                "    INNER JOIN alliances ON (allianceid1 = alliances.id)" + \
                " WHERE allianceid2=" + str(alliance_id)
            oRss = oConnExecuteAll(query)

            if oRss:
                list = []
                for oRs in oRss:
                    item = {}
                    item["wartag"] = oRs[2]
                    item["warname"] = oRs[3]
                    list.append(item)
                    WARcount = NAPcount + 1
                content.AssignValue("wars", list)

            if WARcount == 0:
                content.Parse("nowars")

            #
            # List members that should be displayed
            #

            query = "SELECT rankid, label" + \
                    " FROM alliances_ranks" + \
                    " WHERE members_displayed AND allianceid=" + str(alliance_id) + \
                    " ORDER BY rankid"
            oRss = oConnExecuteAll(query)
            if oRss:
                list = []
                for oRs in oRss:
                    item = {}
                    members = 0
                    item["rank_label"] = oRs[1]

                    query = "SELECT username" + \
                            " FROM users" + \
                            " WHERE alliance_id=" + str(alliance_id) + " AND alliance_rank = " + str(oRs[0]) + \
                            " ORDER BY upper(username)"
                    oMembersRss = oConnExecuteAll(query)

                    item["members"] = []
                    for oMembersRs in oMembersRss:
                        member = {}
                        member["member"] = oMembersRs[0]
                        if members == 0:
                            member["first"] = True
                        else:
                            member["other"] = True

                        members = members + 1
                        item["members"].append(member)

                    if members > 0: list.append(item)

                content.AssignValue("ranks", list)
                
            content.Parse("display")

        return self.Display(content)
