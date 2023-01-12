from .base import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        self.selected_menu = "reports"

        cat = ToInt(request.GET.get("cat", ""), 0)

        return self.display_mails(cat)

    # display list of messages
    def display_mails(self, cat):
        
        content = GetTemplate(self.request, "empire-reports")

        query = "SELECT type, subtype, datetime, battleid, fleetid, fleet_name," + \
                " planetid, planet_name, galaxy, sector, planet," + \
                " researchid, 0, read_date," + \
                " planet_relation, planet_ownername," + \
                " ore, hydrocarbon, credits, scientists, soldiers, workers, username," + \
                " alliance_tag, alliance_name," + \
                " invasionid, spyid, spy_key, description, buildingid," + \
                " upkeep_commanders, upkeep_planets, upkeep_scientists, upkeep_ships, upkeep_ships_in_position, upkeep_ships_parked, upkeep_soldiers," + \
                " name" + \
                " FROM vw_reports" + \
                " WHERE ownerid = " + str(self.UserId)

        #
        # Limit the list to the current category or only display 100 reports if no categories specified
        #
        if cat == 0:
            query = query + " ORDER BY datetime DESC LIMIT 100"
        else:
            query = query + " AND type = "+ str(cat) + " ORDER BY datetime DESC LIMIT 1000"

        content.AssignValue("ownerid", self.UserId)
        
        oRss = oConnExecuteAll(query)
        content.Parse("tabnav_"+str(cat)+"00_selected")
        if oRss == None: content.Parse("noreports")
        else:
            #
            # List the reports returned by the query
            #
            reports = []
            for oRs in oRss:

                reportType = oRs[0]*100+oRs[1]

                if reportType != 140 and reportType != 141 and reportType != 142:
                    report = {}

                    report["type"] = reportType
                    report["date"] = oRs[2]

                    report["battleid"] = oRs[3]
                    report["fleetid"] = oRs[4]
                    report["fleetname"] = oRs[5]
                    report["planetid"] = oRs[6]

                    if oRs[14] in [rHostile, rWar, rFriend]:
                        report["planetname"] = oRs[15]
                    elif oRs[14] in [rAlliance, rSelf]:
                        report["planetname"] = oRs[7]
                    else:
                        report["planetname"] = ""

                    # assign planet coordinates
                    if oRs[8]:
                        report["g"] = oRs[8]
                        report["s"] = oRs[9]
                        report["p"] = oRs[10]

                    report["researchid"] = oRs[11]

                    if oRs[11]: report["researchname"] = getResearchLabel(oRs[11])

                    if oRs[13] == None: report["new"] = True

                    report["ore"] = oRs[16]
                    report["hydrocarbon"] = oRs[17]
                    report["credits"] = oRs[18]

                    report["scientists"] = oRs[19]
                    report["soldiers"] = oRs[20]
                    report["workers"] = oRs[21]

                    report["username"] = oRs[22]
                    report["alliancetag"] = oRs[23]
                    report["alliancename"] = oRs[24]
                    report["invasionid"] = oRs[25]
                    report["spyid"] = oRs[26]
                    report["spykey"] = oRs[27]

                    report["description"] = oRs[28]

                    if oRs[29]: report["building"] = getBuildingLabel(oRs[29])

                    report["upkeep_commanders"] = oRs[30]
                    report["upkeep_planets"] = oRs[31]
                    report["upkeep_scientists"] = oRs[32]
                    report["upkeep_ships"] = oRs[33]
                    report["upkeep_ships_in_position"] = oRs[34]
                    report["upkeep_ships_parked"] = oRs[35]
                    report["upkeep_soldiers"] = oRs[36]

                    report["commandername"] = oRs[37]

                    reports.append(report)
                    
            content.AssignValue("messages", reports)

            #
            # List how many new reports there are for each category
            #
            query = "SELECT r.type, int4(COUNT(1)) " + \
                    " FROM reports AS r" + \
                    " WHERE datetime <= now() AND read_date is null AND r.ownerid = " + str(self.UserId) + \
                    " GROUP BY r.type, r.ownerid, r.read_date"
            oRss = oConnExecuteAll(query)
            
            total_newreports = 0
            for oRs in oRss:
                content.AssignValue("tabnav_"+str(oRs[0])+"00_newreports", oRs[1])
                content.Parse("tabnav_"+str(oRs[0])+"00_new")

                total_newreports = total_newreports + oRs[1]

            if total_newreports != 0:
                content.AssignValue("total_newreports", total_newreports)
                content.Parse("tabnav_000_new")
            
            if not self.IsImpersonating():
                # flag only the current category of reports as read
                if cat != 0:
                    oConnDoQuery("UPDATE reports SET read_date = now() WHERE ownerid = " + str(self.UserId) + " AND type = "+str(cat)+ " AND read_date is null AND datetime <= now()")

                else:
                    oConnDoQuery("UPDATE reports SET read_date = now() WHERE ownerid = " + str(self.UserId) + " AND read_date is null AND datetime <= now()")
            
        content.Parse("tabnav_000")
        content.Parse("tabnav_100")
        content.Parse("tabnav_200")
        content.Parse("tabnav_300")
        content.Parse("tabnav_400")
        content.Parse("tabnav_500")
        content.Parse("tabnav_600")
        content.Parse("tabnav_700")
        content.Parse("tabnav_800")
        content.Parse("tabnav")
        
        return self.Display(content)
