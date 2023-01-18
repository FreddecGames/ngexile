from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "fleets"

        return self.ListShips()

    # List all the available ships for construction
    def ListShips(self):

        # list ships that can be built on the planet
        query = "SELECT category, shipid, killed, lost" + \
                " FROM users_ships_kills" + \
                "    INNER JOIN db_ships ON (db_ships.id = users_ships_kills.shipid)" + \
                " WHERE userid=" + str(self.profile['id']) + \
                " ORDER BY shipid"
        oRss = oConnExecuteAll(query)

        content = getTemplateContext(self.request, "empire-stats")

        count = 0
        kills = 0
        losses = 0
        
        cats = []
        content.assignValue("cats", cats)
        
        lastCategory = -1
        for oRs in oRss:
            
            if oRs[0] != lastCategory:
                
                cat = { "id":oRs[0], "ships":[], "kills":0, "losses":0 }
                cats.append(cat)
                
                lastCategory = oRs[0]

            item = {}
            cat["ships"].append(item)
            
            item["id"] = oRs[1]
            item["name"] = getShipLabel(oRs[1])
            item["killed"] = oRs[2]
            item["lost"] = oRs[3]

            kills += oRs[2]
            losses += oRs[3]
            
            count = count + 1

        if count == 0: content.parse("no_ship")
        else: content.parse("total")
        
        content.assignValue("kills", kills)
        content.assignValue("losses", losses)

        return self.display(content)
