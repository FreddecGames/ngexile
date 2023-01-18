from .base import *


class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "profile"

        return self.display_nation()

    def display_nation_search(self, nation):

        content = getTemplateContext(self.request, "nation-search")

        query = "SELECT username" + \
                " FROM users" + \
                " WHERE upper(username) ILIKE upper(" + str( "\'%" + nation + "%\'") + ")" + \
                " ORDER BY upper(username)"
        oRss = oConnExecuteAll(query)

        list = []
        content.assignValue("nations", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["nation"] = oRs[0]

        return self.display(content)

    def display_nation(self):

        nation = self.request.GET.get("name", "").strip()

        # if no nation is given: display info on the current player
        if nation == "": nation = self.oPlayerInfo["username"]

        content = getTemplateContext(self.request, "profile-view")

        query = "SELECT u.username, u.avatar_url, u.description, sp_relation(u.id, "+str(self.profile['id'])+"), " + \
                " u.alliance_id, a.tag, a.name, u.id, GREATEST(u.regdate, u.game_started) AS regdate, r.label," + \
                " COALESCE(u.alliance_joined, u.regdate), u.alliance_taxes_paid, u.alliance_credits_given, u.alliance_credits_taken," + \
                " u.id" + \
                " FROM users AS u" + \
                " LEFT JOIN alliances AS a ON (u.alliance_id = a.id) " + \
                " LEFT JOIN alliances_ranks AS r ON (u.alliance_id = r.allianceid AND u.alliance_rank = r.rankid) " + \
                " WHERE upper(u.username) = upper(" + strSql(nation) + ") LIMIT 1"
        oRs = oConnExecute(query)

        if oRs == None:
            if nation != "":
                return HttpResponseRedirect('/s03/profile-view/')
            else:
                return HttpResponseRedirect("/s03/profile-view/")

        nationId = oRs[7]

        content.assignValue("name", oRs[0])
        content.assignValue("regdate", oRs[8])

        content.assignValue("alliance_joined", oRs[10])

        if oRs[1] == None or oRs[1] == "":
            content.parse("noavatar")
        else:
            content.assignValue("avatar_url", oRs[1])
            content.parse("avatar")

        if oRs[7] != self.profile['id']: content.parse("sendmail")

        if oRs[2] and oRs[2] != "":
            content.assignValue("description", oRs[2])

        if oRs[3] < rFriend:
            content.parse("enemy")
        elif oRs[3] == rFriend:
            content.parse("friend")
        elif oRs[3] > rFriend:  # display planets + fleets of alliance members if has the rights for it

            if oRs[3] == rAlliance:
                content.parse("ally")
                show_details = self.oAllianceRights["leader"] or self.oAllianceRights["can_see_members_info"]
            else:
                content.parse("self")
                show_details = True

            if show_details:
                if oRs[3] == rAlliance:
                    if not self.oAllianceRights["leader"]:
                        show_details = False

                if show_details:
                    # view current nation planets
                    query = "SELECT name, galaxy, sector, planet FROM vw_planets WHERE ownerid=" + str(oRs[7])
                    query = query + " ORDER BY id"
                    oPlanetsRs = oConnExecuteAll(query)

                    if oPlanetsRs == None:
                        content.parse("noplanets")

                    planets = []
                    content.assignValue("planets", planets)
                    for rs in oPlanetsRs:
                        i = {}
                        planets.append(i)
                        i["planetname"] = rs[0]
                        i["g"] = rs[1]
                        i["s"] = rs[2]
                        i["p"] = rs[3]

                # view current nation fleets

                query = "SELECT id, name, attackonsight, engaged, remaining_time, " + \
                    " planetid, planet_name, planet_galaxy, planet_sector, planet_planet, planet_ownerid, planet_owner_name, sp_relation(planet_ownerid, ownerid)," + \
                    " destplanetid, destplanet_name, destplanet_galaxy, destplanet_sector, destplanet_planet, destplanet_ownerid, destplanet_owner_name, sp_relation(destplanet_ownerid, ownerid)," + \
                    " action, signature, sp_get_user_rs(ownerid, planet_galaxy, planet_sector), sp_get_user_rs(ownerid, destplanet_galaxy, destplanet_sector)" + \
                    " FROM vw_fleets WHERE ownerid=" + str(oRs[7])

                if oRs[3] == rAlliance:
                    if not self.oAllianceRights["leader"]:
                        query = query + " AND action != 0"

                query = query + " ORDER BY planetid, upper(name)"

                oFleetsRs = oConnExecuteAll(query)

                if oFleetsRs == None: content.parse("nofleets")

                fleets = []
                content.assignValue("fleets", fleets)
                for rs in oFleetsRs:
                    i = {}
                    fleets.append(i)
                    i["fleetid"] = rs[0]
                    i["fleetname"] = rs[1]
                    i["planetid"] = rs[5]
                    i["signature"] = rs[22]
                    i["g"] = rs[7]
                    i["s"] = rs[8]
                    i["p"] = rs[9]
                    if rs[4]:
                        i["time"] = rs[4]
                    else:
                        i["time"] = 0

                    i["relation"] = rs[12]
                    i["planetname"] = getPlanetName(rs[12], rs[23], rs[11], rs[6])

                    if oRs[3] == rAlliance:
                        i["ally"] = True
                    else:
                        i["owned"] = True

                    if rs[3]:
                        i["fighting"] = True
                    elif rs[21]==2:
                        i["recycling"] = True
                    elif rs[13]:
                        # Assign destination planet
                        i["t_planetid"] = rs[13]
                        i["t_g"] = rs[15]
                        i["t_s"] = rs[16]
                        i["t_p"] = rs[17]
                        i["t_relation"] = rs[20]
                        i["t_planetname"] = getPlanetName(rs[20], rs[24], rs[19], rs[14])

                        i["moving"] = True
                    else:
                        i["patrolling"] = True

                content.parse("allied")

        if oRs[4] != None:
            content.assignValue("alliancename", oRs[6])
            content.assignValue("alliancetag", oRs[5])
            content.assignValue("rank_label", oRs[9])

            if oRs[3] == rSelf:
                content.parse("self")
            elif oRs[3] == rAlliance:
                content.parse("ally")
            elif oRs[3] == rFriend:
                content.parse("friend")
            else:
                content.parse("enemy")

            content.parse("alliance")
        else:
            content.parse("noalliance")

        query = "SELECT alliance_tag, alliance_name, joined, \"left\"" + \
                " FROM users_alliance_history" + \
                " WHERE userid = " + str(nationId) + " AND joined > (SELECT GREATEST(regdate, game_started) FROM users WHERE privilege < 100 AND id=" + str(nationId) + ")" + \
                " ORDER BY joined DESC"
        oRss = oConnExecuteAll(query)

        list = []
        content.assignValue("alliances", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["history_tag"] = oRs[0]
            item["history_name"] = oRs[1]
            item["joined"] = oRs[2]
            item["left"] = oRs[3]

        return self.display(content)
