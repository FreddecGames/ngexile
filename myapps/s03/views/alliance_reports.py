from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "alliance"

        cat = ToInt(request.GET.get("cat"), 0)

        if self.AllianceId == None: return HttpResponseRedirect("/s03/alliance-view/")
        if not self.oAllianceRights["can_see_reports"]: return HttpResponseRedirect("/s03/alliance-view/")

        return self.display_reports(cat)

    # display list of messages
    def display_reports(self, cat):

        content = GetTemplate(self.request, "empire-reports")

        query = "SELECT type, subtype, datetime, battleid, fleetid, fleet_name," + \
                " planetid, planet_name, galaxy, sector, planet," + \
                " researchid, 0, read_date," + \
                " planet_relation, planet_ownername," + \
                " ore, hydrocarbon, credits, scientists, soldiers, workers, username," + \
                " alliance_tag, alliance_name," + \
                " invasionid, spyid, spy_key, description, ownerid, invited_username, username, buildingid" + \
                " FROM vw_alliances_reports" + \
                " WHERE ownerallianceid = " + str(self.AllianceId)

        #
        # Limit the list to the current category or only display 100 reports if no categories specified
        #
        if cat == 0:
            query = query + " ORDER BY datetime DESC LIMIT 200"
        else:
            query = query + " AND type = "+ str(cat) + " ORDER BY datetime DESC LIMIT 200"

        oRss = oConnExecuteAll(query)
        content.Parse("tabnav_"+str(cat)+"00_selected")
        if oRss == None: content.Parse("noreports")
        else:
            #
            # List the reports returned by the query
            #
            list = []
            content.AssignValue('messages', list)
            for oRs in oRss:
                reportType = oRs[0]*100+oRs[1]
                if reportType != 133:
                    
                    item = {}
                    list.append(item)
                    
                    item["ownerid"] = oRs[29]
                    item["invitedusername"] = oRs[30]
                    item["nation"] = oRs[31]
        
                    item["type"] = oRs[0]*100+oRs[1]
                    item["date"] = oRs[2]
        
                    item["battleid"] = oRs[3]
                    item["fleetid"] = oRs[4]
                    item["fleetname"] = oRs[5]
                    item["planetid"] = oRs[6]
        
                    if oRs[14] in [rHostile, rWar]:
                        item["planetname"] = oRs[15]
                    elif oRs[14] in [rFriend, rAlliance, rSelf]:
                        item["planetname"] = oRs[7]
                    else:
                        item["planetname"] = ""
        
                        # assign planet coordinates
                    if oRs[8]:
                        item["g"] = oRs[8]
                        item["s"] = oRs[9]
                        item["p"] = oRs[10]
        
                    item["researchid"] = oRs[11]
                    if (oRs[11]): item["researchname"] = getResearchLabel(oRs[11])
        
                    item["ore"] = oRs[16]
                    item["hydrocarbon"] = oRs[17]
                    item["credits"] = oRs[18]
        
                    item["scientists"] = oRs[19]
                    item["soldiers"] = oRs[20]
                    item["workers"] = oRs[21]
        
                    item["username"] = oRs[22]
                    item["alliancetag"] = oRs[23]
                    item["alliancename"] = oRs[24]
                    item["invasionid"] = oRs[25]
                    item["spyid"] = oRs[26]
                    item["spykey"] = oRs[27]
        
                    item["description"] = oRs[28]
        
                    if (oRs[32]): item["building"] = getBuildingLabel(oRs[32])
    
        content.Parse("tabnav_000")
        content.Parse("tabnav_100")
        content.Parse("tabnav_200")
        content.Parse("tabnav_800")
        content.Parse("tabnav")

        return self.Display(content)
