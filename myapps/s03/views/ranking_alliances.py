from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "ranking"

        content = GetTemplate(self.request, "ranking-alliances")

        query = "SELECT alliances.id, alliances.tag, alliances.name," + \
                " sum(users.score) AS alliance_score, sum(users.score - users.previous_score) AS alliance_score_delta," + \
                " count(*) AS members, sum(planets) AS planets" + \
                " FROM users INNER JOIN alliances ON alliances.id = alliance_id" + \
                " GROUP BY alliances.id, alliances.name, alliances.tag" + \
                " ORDER BY alliance_score DESC"
        dbRows = oConnRows(query)

        list = []
        content.AssignValue("alliances", list)

        i = 1
        for dbRow in dbRows:
        
            item = {}
            list.append(item)
            
            item["place"] = i
            
            item["tag"] = dbRow["tag"]
            item["name"] = dbRow["name"]
            item["score"] = dbRow["alliance_score"]
            item["score_delta"] = dbRow["alliance_score_delta"]
            item["members"] = dbRow["members"]
            item["planets"] = dbRow["planets"]

            if self.AllianceId and dbRow["id"] == self.AllianceId: item["player_alliance"] = True

            i = i + 1

        return self.Display(content)
