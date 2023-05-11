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
        
        action = request.GET.get("a", "").lower()
        
        if action == "research":
            
            #---
            
            researchId = ToInt(request.GET.get("r"), 0)
            dbQuery("SELECT * FROM sp_start_research(" + str(self.userId) + ", " + str(researchId) + ", false)")
            
            return HttpResponseRedirect('/s03/tech-list/')
            
        elif action == "cancel":
        
            #---
            
            researchId = ToInt(request.GET.get("r"), 0)
            dbQuery("SELECT * FROM sp_cancel_research(" + str(self.userId) + ", " + str(researchId) + ")")
            
            return HttpResponseRedirect('/s03/tech-list/')
        
        elif action == "continue":
        
            #---
            
            researchId = ToInt(request.GET.get("r"), 0)
            dbQuery("UPDATE researches_pending SET looping=true WHERE userid=" + str(self.userId) + " AND researchid=" + str(researchId))
            
            return HttpResponseRedirect('/s03/tech-list/')
        
        elif action == "stop":
        
            #---
            
            researchId = ToInt(request.GET.get("r"), 0)
            dbQuery("UPDATE researches_pending SET looping=false WHERE userid=" + str(self.userId) + " AND researchid=" + str(researchId))
            
            return HttpResponseRedirect('/s03/tech-list/')
                
        #---
        
        dbQuery("SELECT sp_update_researches(" + str(self.userId) + ")")
        
        #---
        
        self.selectedMenu = "research"

        content = getTemplate(request, "s03/research")

        #---
        
        underResearchCount = dbExecute("SELECT int4(count(1)) FROM researches_pending WHERE userid=" + str(self.userId) + " LIMIT 1")

        #---
        
        query = "SELECT researchid AS id, t.category, total_cost, total_time, level, (level + 1) AS nextlevel, t.levels, researchable, buildings_requirements_met, status," + \
                " (SELECT looping FROM researches_pending WHERE researchid = t.researchid AND userid=" + str(self.userId) + ") AS looping," + \
                " expiration_time IS NOT NULL, db_research.label, db_research.description" + \
                " FROM sp_list_researches(" + str(self.userId) + ") AS t" + \
                "   INNER JOIN db_research ON db_research.id = researchid" + \
                " WHERE level > 0 OR (researchable AND planet_elements_requirements_met AND buildings_requirements_met)" + \
                " ORDER BY t.category"
        rows = dbRows(query)
        
        categories = []
        content.setValue("categories", categories)
        
        lastCategory = -1        
        for row in rows:
        
            catId = row['category']
            if catId != lastCategory:
                lastCategory = catId
            
                category = { 'id':catId, 'researches':[] }
                categories.append(category)

            category['researches'].append(row)
            
            if row['level'] >= row['levels']:
                row['total_cost'] = 0
                row['total_time'] = 0
                
            if not self.profile["credits"] >= row['total_cost']: row["notenoughmoney"] = True
            
            if underResearchCount <= 0: row['can_research'] = True
            
        #---
        
        return self.display(content, request)
