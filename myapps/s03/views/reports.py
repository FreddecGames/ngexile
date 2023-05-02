# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        #---
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        #---
        
        self.selectedMenu = "reports"
        
        content = getTemplate(request, "s03/reports")

        #---

        content.setValue("ownerid", self.userId)

        #---

        cat = ToInt(request.GET.get("cat", ""), 0)
        content.setValue("cat", cat)
        
        #---
        
        query = "SELECT type, subtype, datetime AS date, battleid, fleetid, fleet_name AS fleetname," + \
                " planetid, planet_name, galaxy, sector, planet," + \
                " researchid, 0, read_date," + \
                " planet_relation, planet_ownername," + \
                " ore, hydrocarbon, credits, scientists, soldiers, workers, username," + \
                " alliance_tag AS alliancetag, alliance_name AS alliancename," + \
                " invasionid, spyid, spy_key AS spykey, description, buildingid," + \
                " upkeep_commanders, upkeep_planets, upkeep_scientists, upkeep_ships, upkeep_ships_in_position, upkeep_ships_parked, upkeep_soldiers," + \
                " name AS commandername" + \
                " FROM vw_reports" + \
                " WHERE ownerid = " + str(self.userId)
        if cat == 0: query = query + " ORDER BY datetime DESC LIMIT 100"
        else: query = query + " AND type = " + str(cat) + " ORDER BY datetime DESC LIMIT 1000"        
        rows = dbRows(query)

        reports = []
        content.setValue("reports", reports)
        
        for oRs in rows:

            reportType = oRs['type'] * 100 + oRs['subtype']
            if reportType != 140 and reportType != 141 and reportType != 142 and reportType != 133:
            
                report = oRs
                reports.append(report)

                report["type"] = reportType

                if oRs['planet_relation'] in [rHostile, rWar, rFriend]: report["planetname"] = oRs['planet_ownername']
                elif oRs['planet_relation'] in [rAlliance, rSelf]: report["planetname"] = oRs['planet_name']
                else: report["planetname"] = ""
                    
        #---
        
        query = "SELECT r.type, int4(COUNT(1))AS count " + \
                " FROM reports AS r" + \
                " WHERE datetime <= now()" + \
                " GROUP BY r.type, r.ownerid, r.read_date" + \
                " HAVING r.ownerid = " + str(self.userId) + " AND read_date is null"
        rows = dbRows(query)
        
        total_newreports = 0
        
        for row in rows:
        
            content.setValue("tabnav_" + str(row['type']) + "00_newreports", row['count'])

            total_newreports += row['count']
        
        content.setValue("total_newreports", total_newreports)
        
        #---
        
        if not request.user.is_impersonate:

            if cat != 0:
                dbQuery("UPDATE reports SET read_date = now() WHERE ownerid = " + str(self.userId) + " AND type = " + str(cat) + " AND read_date is null AND datetime <= now()")

            if request.GET.get("cat", "") == "0":
                dbQuery("UPDATE reports SET read_date = now() WHERE ownerid = " + str(self.userId) + " AND read_date is null AND datetime <= now()")

        #---

        return self.display(content, request)
