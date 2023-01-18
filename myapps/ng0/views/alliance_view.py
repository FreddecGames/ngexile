from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "alliance"

        tag = request.GET.get("tag")

        if tag and tag != "":
            return self.DisplayAlliance(tag)
        else:
            if self.AllianceId == None:
                return HttpResponseRedirect("/s03/alliance-invitations/")
            else:
                return self.DisplayAlliance(None)

    def DisplayAlliance(self, alliance_tag):

        content = getTemplateContext(self.request, "alliance-view")

        self.selectedMenu = "alliance"

        query = "SELECT id, name, tag, description, created, (SELECT count(*) FROM users WHERE alliance_id=alliances.id)," + \
                " logo_url, website_url, max_members, credits" + \
                " FROM alliances"

        if alliance_tag == None:
            query = query + " WHERE id=" + str(self.AllianceId) + " LIMIT 1"
        else:
            query = query + " WHERE tag=upper(" + strSql(alliance_tag) + ") LIMIT 1"
            self.selectedMenu = "ranking"

        oRs = oConnExecute(query)

        if oRs:
            alliance_id = oRs[0]
            content.assignValue("name", oRs[1])
            content.assignValue("tag", oRs[2])
            content.assignValue("description", oRs[3])

            created = oRs[4]
            content.assignValue("created", created)
            content.assignValue("members", oRs[5])
            content.assignValue("max_members", oRs[8])
            content.assignValue("alliance_credits", oRs[9])

            if oRs[6] and oRs[6] != "":
                content.assignValue("logo_url", oRs[6])
                content.parse("logo")

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
                content.assignValue("naps", list)

            if NAPcount == 0:
                content.parse("nonaps")

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
                content.assignValue("wars", list)

            if WARcount == 0:
                content.parse("nowars")

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

                content.assignValue("ranks", list)
                
            content.parse("display")
            content.assignValue("allianceId", self.AllianceId)

        return self.display(content)
