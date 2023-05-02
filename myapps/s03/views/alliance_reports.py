# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not self.allianceId or not (self.allianceRights["leader"] or self.allianceRights["can_see_reports"]):
            return HttpResponseRedirect('/s03/alliance/')
        
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, *args, **kwargs):

        content = getTemplate(request, "s03/alliance-reports")
        
        self.selectedMenu = "alliance.reports"
        
        #---

        query = "SELECT type, subtype, datetime, battleid, fleetid, fleet_name," + \
                " planetid, planet_name, galaxy, sector, planet," + \
                " researchid, 0, read_date," + \
                " planet_relation, planet_ownername," + \
                " ore, hydrocarbon, credits, scientists, soldiers, workers, username," + \
                " alliance_tag, alliance_name," + \
                " invasionid, spyid, spy_key, description, ownerid, invited_username, login, buildingid" + \
                " FROM vw_alliances_reports" + \
                " WHERE ownerallianceid = " + str(self.allianceId) + " ORDER BY datetime DESC LIMIT 200"
        reports = dbRows(query)
        content.setValue("reports", reports)

        for report in reports:
            report['type'] = report['type'] * 100 + report['subtype']

        return self.display(content, request)
