# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        self.selected_menu = "research"

        oConnExecute("SELECT sp_update_researches(" + str(self.UserId) + ")")

        Action = request.GET.get("a", "").lower()
        ResearchId = ToInt(request.GET.get("r"), 0)

        if ResearchId != 0:

            if Action == "research":
                self.StartResearch(ResearchId)
            elif Action == "cancel":
                self.CancelResearch(ResearchId)
            elif Action == "continue":
                oConnDoQuery("UPDATE researches_pending SET looping=true WHERE userid=" + str(self.UserId) + " AND researchid=" + str(ResearchId))
            elif Action == "stop":
                oConnDoQuery("UPDATE researches_pending SET looping=false WHERE userid=" + str(self.UserId) + " AND researchid=" + str(ResearchId))
                
        return self.ListResearches()

    def HasEnoughFunds(self, credits):
        return credits <= 0 or self.oPlayerInfo["credits"] >= credits

    # List all the available researches
    def ListResearches(self):

        # count number of researches pending
        oRs = oConnExecute("SELECT int4(count(1)) FROM researches_pending WHERE userid=" + str(self.UserId) + " LIMIT 1")
        underResearchCount = oRs[0]

        # list things that can be researched
        query = "SELECT researchid, category, total_cost, total_time, level, levels, researchable, buildings_requirements_met, status," + \
                " (SELECT looping FROM researches_pending WHERE researchid = t.researchid AND userid=" + str(self.UserId) + ") AS looping," + \
                " expiration_time IS NOT NULL" + \
                " FROM sp_list_researches(" + str(self.UserId) + ") AS t" + \
                " WHERE level > 0 OR (researchable AND planet_elements_requirements_met)"
        oRss = oConnExecute(query)
        
        content = GetTemplate(self.request, "s03/research")

        content.AssignValue("userid", self.UserId)

        # number of items in category
        itemCount = 0
        
        lastCategory = -1
        
        categories = []
        for oRs in oRss:
            CatId = oRs[1]

            if CatId != lastCategory:
                category = {'id':CatId, 'researches':[]}
                categories.append(category)
                lastCategory = CatId
                itemCount = 0
            
            research = {}
            category['researches'].append(research)
            
            itemCount = itemCount + 1

            research["id"] = oRs[0]
            research["name"] = getResearchLabel(oRs[0])
            research["credits"] = oRs[2]
            research["nextlevel"] = oRs[4]+1
            research["level"] = oRs[4]
            research["levels"] = oRs[5]
            research["description"] = getResearchDescription(oRs[0])

            status = oRs[8]

            # if status is not None: this research is under way
            if status:
                if status < 0: status = 0

                research["leveling"] = True

                research["remainingtime"] = status

                if oRs[9]:
                    research["auto"] = True
                else:
                    research["manual"] = True

                research["cost"] = True
                research["countdown"] = True
                research["researching"] = True
            else:

                if (oRs[4] < oRs[5] or oRs[10]):
                    research["time"] = oRs[3]
                    research["researchtime"] = True

                    if not oRs[6] or not oRs[7]:
                        research["notresearchable"] = True
                    elif underResearchCount > 0:
                        research["busy"] = True
                    elif not self.HasEnoughFunds(oRs[2]):
                        research["notenoughmoney"] = True
                    else:
                        research["research"] = True

                    research["cost"] = True
                else:
                    research["nocost"] = True
                    research["noresearchtime"] = True
                    research["complete"] = True

        content.AssignValue("categories", categories)
        
        self.FillHeaderCredits(content)

        return self.Display(content)

    def StartResearch(self, ResearchId):
        oConnExecute("SELECT * FROM sp_start_research(" + str(self.UserId) + ", " + str(ResearchId) + ", false)")

    def CancelResearch(self, ResearchId):
        oConnExecute("SELECT * FROM sp_cancel_research(" + str(self.UserId) + ", " + str(ResearchId) + ")")
