from .base import *


class View(BaseView):
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response:
            return response

        self.selectedMenu = "reports"

        invasionid = toInt(request.GET.get("id"), 0)

        if invasionid == 0:
            return HttpResponseRedirect("/s03/empire-view/")

        self.fleetid = toInt(request.GET.get("fleetid"), 0)

        return self.DisplayReport(invasionid, self.profile['id'])

    def DisplayReport(self, invasionid, readerid):

        content = getTemplateContext(self.request, "report-invasion")

        query = (
            "SELECT i.id, i.time, i.planet_id, i.planet_name, i.attacker_name, i.defender_name, "
            + "i.attacker_succeeded, i.soldiers_total, i.soldiers_lost, i.def_soldiers_total, "
            + "i.def_soldiers_lost, i.def_scientists_total, i.def_scientists_lost, i.def_workers_total, "
            + "i.def_workers_lost, galaxy, sector, planet, sp_get_user("
            + str(readerid)
            + ") "
            + "FROM invasions AS i INNER JOIN nav_planet ON nav_planet.id = i.planet_id WHERE i.id = "
            + str(invasionid)
        )
        oRs = oConnExecute(query)

        if oRs == None:
            return HttpResponseRedirect("/s03/empire-view/")

        viewername = oRs[18]

        # compare the attacker name and defender name with the name of who is reading this report
        if oRs[4] != viewername and oRs[5] != viewername and self.AllianceId:
            # if we are not the attacker or defender, check if we can view this invasion as a member of our alliance of we are ambassador
            if self.oAllianceRights["can_see_reports"]:
                # find the name of the member that did this invasion, either the attacker or the defender
                query = (
                    "SELECT username"
                    + " FROM users"
                    + " WHERE (username="
                    + strSql(oRs[4])
                    + " OR username="
                    + strSql(oRs[5])
                    + ") AND alliance_id="
                    + str(self.AllianceId)
                    + " AND alliance_joined <= (SELECT time FROM invasions WHERE id="
                    + str(invasionid)
                    + ")"
                )
                oRs2 = oConnExecute(query)
                if oRs2 == None:
                    return HttpResponseRedirect("/s03/empire-view/")
                viewername = oRs2[0]
            else:
                return HttpResponseRedirect("/s03/empire-view/")

        content.assignValue("planetid", oRs[2])
        content.assignValue("planetname", oRs[3])
        content.assignValue("g", oRs[15])
        content.assignValue("s", oRs[16])
        content.assignValue("p", oRs[17])
        content.assignValue("planet_owner", oRs[5])
        content.assignValue("fleet_owner", oRs[4])
        content.assignValue("date", oRs[1])
        content.assignValue("soldiers_total", oRs[7])
        content.assignValue("soldiers_lost", oRs[8])
        content.assignValue("soldiers_alive", oRs[7] - oRs[8])
        content.assignValue("def_soldiers_total", oRs[9])
        content.assignValue("def_soldiers_lost", oRs[10])
        content.assignValue("def_soldiers_alive", oRs[9] - oRs[10])
        def_total = oRs[9]
        def_losts = oRs[10]

        if oRs[4] == viewername:  # we are the attacker
            content.assignValue("relation", rWar)
            # display only troops encountered by the attacker's soldiers
            if oRs[9] - oRs[10] == 0:
                # if no workers remain, display the scientists
                if oRs[13] - oRs[14] == 0:
                    def_total = def_total + oRs[11]
                    def_losts = def_losts + oRs[12]
                    content.assignValue("def_scientists_total", oRs[11])
                    content.assignValue("def_scientists_lost", oRs[12])
                    content.assignValue("def_scientists_alive", oRs[11] - oRs[12])
                    content.parse("scientists")

                # if no soldiers remain, display the workers
                def_total = def_total + oRs[13]
                def_losts = def_losts + oRs[14]
                content.assignValue("def_workers_total", oRs[13])
                content.assignValue("def_workers_lost", oRs[14])
                content.assignValue("def_workers_alive", oRs[13] - oRs[14])
                content.parse("workers")

            content.assignValue("planetname", oRs[5])

            content.assignValue("def_alive", def_total - def_losts)
            content.assignValue("def_total", def_total)
            content.assignValue("def_losts", def_losts)

            content.parse("ally")
            content.parse("attacker")
            content.parse("enemy")
            content.parse("defender")
        else:  # ...we are the defender
            content.assignValue("relation", rFriend)
            def_total = def_total + oRs[11]
            def_losts = def_losts + oRs[12]
            content.assignValue("def_scientists_total", oRs[11])
            content.assignValue("def_scientists_lost", oRs[12])
            content.assignValue("def_scientists_alive", oRs[11] - oRs[12])
            content.parse("scientists")
            def_total = def_total + oRs[13]
            def_losts = def_losts + oRs[14]
            content.assignValue("def_workers_total", oRs[13])
            content.assignValue("def_workers_lost", oRs[14])
            content.assignValue("def_workers_alive", oRs[13] - oRs[14])
            content.parse("workers")

            content.assignValue("def_alive", def_total - def_losts)
            content.assignValue("def_total", def_total)
            content.assignValue("def_losts", def_losts)

            content.parse("ally")
            content.parse("defender")
            content.parse("enemy")
            content.parse("attacker")

        if self.fleetid != 0:
            # if a fleetid is specified, parse a link to redirect the user to the fleet
            content.assignValue("fleetid", self.fleetid)
            content.parse("justdone")

        if oRs[6]:
            content.parse("succeeded")
        else:
            content.parse("not_succeeded")

        content.parse("report")
        content.parse("invasion_report")

        return self.display(content)
