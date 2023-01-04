from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "working"

        self.showHeader = True

        return self.displayPage(True)

    def displayManage(self):

        if self.action == "submit":
            query = "SELECT buildingid, quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END, disabled" + \
                    " FROM planet_buildings" + \
                    "    INNER JOIN db_buildings ON (planet_buildings.buildingid=db_buildings.id)" + \
                    " WHERE can_be_disabled AND planetid=" + str(self.CurrentPlanet)
            oRss = oConnExecuteAll(query)
            for oRs in oRss:

                quantity = oRs[1] - ToInt(self.request.POST.get("enabled" + str(oRs[0])), 0)

                query = "UPDATE planet_buildings SET" + \
                        " disabled=LEAST(quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END, " + str(quantity) + ")" + \
                        "WHERE planetid=" + str(self.CurrentPlanet) + " AND buildingid =" + str(oRs[0])
                oConnDoQuery(query)

            return HttpResponseRedirect("/s03/planet-working/?cat=" + str(self.cat))

        query = "SELECT buildingid, quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END, disabled, energy_consumption, int4(workers*maintenance_factor/100.0), upkeep" + \
                " FROM planet_buildings" + \
                "    INNER JOIN db_buildings ON (planet_buildings.buildingid=db_buildings.id)" + \
                " WHERE can_be_disabled AND planetid=" + str(self.CurrentPlanet) + \
                " ORDER BY buildingid"
        oRss = oConnExecuteAll(query)

        list = []
        self.content.AssignValue("buildings", list)
        for oRs in oRss:
            if oRs[1] > 0:
                item = {}
                list.append(item)
                
                enabled = oRs[1] - oRs[2]
                quantity = oRs[1] - oRs[2]*0.95

                item["id"] = oRs[0]
                item["building"] = getBuildingLabel(oRs[0])
                item["quantity"] = oRs[1]
                item["energy"] = oRs[3]
                item["maintenance"] = oRs[4]
                item["upkeep"] = oRs[5]
                item["energy_total"] = round(quantity * oRs[3])
                item["maintenance_total"] = round(quantity * oRs[4])
                item["upkeep_total"] = round(quantity * oRs[5])

                if oRs[2] > 0: item["not_all_enabled"] = True

                item["counts"] = []
                for i in range(0, oRs[1] + 1):
                    data = {}
                    data["count"] = i
                    if i == enabled: data["selected"] = True
                    item["enable"] = True
                    item["counts"].append(data)

        self.content.Parse("manage")

    def displayPage(self, RecomputeIfNeeded):
        self.action = self.request.GET.get("a")
        self.cat = ToInt(self.request.GET.get("cat"), 1)
        if self.cat < 1 or self.cat > 3: self.cat = 1

        self.content = GetTemplate(self.request, "planet-working")
        self.content.AssignValue("cat", self.cat)

        response = self.displayManage()
        if response: return response
        self.content.Parse("cat2_selected")

        self.content.Parse("cat1")
        self.content.Parse("cat2")
        self.content.Parse("cat3")
        self.content.Parse("nav")

        url_extra_params = "cat=" + str(self.cat)

        return self.Display(self.content)