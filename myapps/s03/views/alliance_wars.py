# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "alliance.wars"

        self.result = ""
        self.cease_success = ""

        cat = ToInt(request.GET.get("cat"), 0)
        if cat < 1 or cat > 2: cat = 1

        if not (self.oAllianceRights["can_create_nap"] or self.oAllianceRights["can_break_nap"]) and cat != 1: cat = 1

        #
        # Process actions
        #

        # redirect the player to the alliance page if he is not part of an alliance
        if self.AllianceId == None:
            return HttpResponseRedirect("/s03/alliance/")

        action = request.GET.get("a", "")
        self.tag = ""

        if action == "pay":
            tag = request.GET.get("tag", "").strip()
            oRs = oConnExecute("SELECT sp_alliance_war_pay_bill(" + str(self.userId) + "," + dosql(self.tag) + ")")

            if oRs[0] == 0:
                self.cease_success = "ok"
            elif oRs[0] == 1:
                self.cease_success = "norights"
            elif oRs[0] == 2:
                self.cease_success = "unknown"
            elif oRs[0] == 3:
                self.cease_success = "war_not_found"

        elif action == "stop":
            self.tag = request.GET.get("tag", "").strip()
            oRs = oConnExecute("SELECT sp_alliance_war_stop(" + str(self.userId) + "," + dosql(self.tag) + ")")

            if oRs[0] == 0:
                self.cease_success = "ok"
            elif oRs[0] == 1:
                self.cease_success = "norights"
            elif oRs[0] == 2:
                self.cease_success = "unknown"
            elif oRs[0] == 3:
                self.cease_success = "war_not_found"

        elif action == "new2":
            self.tag = request.POST.get("tag", "").strip()

            oRs = oConnExecute("SELECT sp_alliance_war_declare(" + str(self.userId) + "," + dosql(self.tag) + ")")
            if oRs[0] == 0:
                self.result = "ok"
                self.tag = ""
            elif oRs[0] == 1:
                self.result = "norights"
            elif oRs[0] == 2:
                self.result = "unknown"
            elif oRs[0] == 3:
                self.result = "already_at_war"
            elif oRs[0] == 9:
                self.result = "not_enough_credits"

        return self.displayPage(cat)

    def displayWars(self, content):
        col = ToInt(self.request.GET.get("col"), 0)
        if col < 1 or col > 2: col = 1

        reversed = False
        if col == 1:
            orderby = "tag"
        elif col == 2:
            orderby = "created"
            reversed = True
        content.setValue("col", col)

        if self.request.GET.get("r", "") != "":
            reversed = not reversed
        else:
            content.Parse("r" + str(col))

        if reversed: orderby = orderby + " DESC"
        orderby = orderby + ", tag"

        # List wars
        query = "SELECT w.created, alliances.id, alliances.tag, alliances.name, cease_fire_requested, date_part('epoch', cease_fire_expire-now())::integer, w.can_fight < now() AS can_fight, True AS attacker, next_bill < now() + INTERVAL '1 week', sp_alliance_war_cost(allianceid2), next_bill"+ \
                " FROM alliances_wars w" + \
                "    INNER JOIN alliances ON (allianceid2 = alliances.id)" + \
                " WHERE allianceid1=" + str(self.AllianceId) + \
                " UNION " + \
                "SELECT w.created, alliances.id, alliances.tag, alliances.name, cease_fire_requested, date_part('epoch', cease_fire_expire-now())::integer, w.can_fight < now() AS can_fight, False AS attacker, False, 0, next_bill"+ \
                " FROM alliances_wars w" + \
                "    INNER JOIN alliances ON (allianceid1 = alliances.id)" + \
                " WHERE allianceid2=" + str(self.AllianceId) + \
                " ORDER BY " + orderby
        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.setValue("wars", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["place"] = i+1
            item["created"] = oRs[0]
            item["tag"] = oRs[2]
            item["name"] = oRs[3]

            if self.oAllianceRights["can_break_nap"]:
                if oRs[4] == None:
                    if oRs[7]:
                        if oRs[8]:
                            item["cost"] = oRs[9]
                            item["extend"] = True

                        item["stop"] = True

                elif oRs[4] == self.AllianceId:
                    item["time"] = oRs[5]
                    item["ceasing"] = True
                else:
                    item["time"] = oRs[5]
                    item["cease_requested"] = True

            if oRs[6]:
                item["next_bill"] = oRs[10]
                if oRs[10]:
                    item["can_fight"] = True

            else:
                item["cant_fight"] = True

            i = i + 1

        if self.oAllianceRights["can_break_nap"] and (i > 0): content.Parse("cease")

        if i == 0: content.Parse("nowars")

        if self.cease_success != "":
            content.Parse("cease_success")
            content.Parse("message")

    def displayDeclaration(self, content):
        if self.request.GET.get("a", "") == "new":

            self.tag = self.request.POST.get("tag").strip()

            oRs = oConnExecute("SELECT id, tag, name, sp_alliance_war_cost(id) + (const_coef_score_to_war()*sp_alliance_value(" + str(self.AllianceId) + "))::integer FROM alliances WHERE lower(tag)=lower(" + dosql(self.tag) + ")")
            if oRs == None:
                content.setValue("tag", self.tag)

                content.Parse("unknown")
                content.Parse("message")
                content.Parse("newwar")
            else:
                content.setValue("tag", oRs[1])
                content.setValue("name", oRs[2])
                content.setValue("cost", oRs[3])

                content.Parse("newwar_confirm")

        else:
            if self.result != "":
                content.Parse(self.result)
                content.Parse("message")

            content.setValue("tag", self.tag)

            content.Parse("newwar")

    def displayPage(self, cat):
        content = getTemplate(self.request, "s03/alliance-wars")
        content.setValue("cat", cat)

        if cat == 1:
            self.displayWars(content)
        elif cat == 2:
            self.displayDeclaration(content)

        content.Parse("cat" + str(cat) + "_selected")

        content.Parse("cat1")
        if self.oAllianceRights["can_create_nap"]: content.Parse("cat2")
        content.Parse("nav")

        return self.display(content)
