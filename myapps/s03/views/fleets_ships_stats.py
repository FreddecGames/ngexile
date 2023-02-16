# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "fleets_ships_stats"

        return self.ListShips()

    # List all the available ships for construction
    def ListShips(self):

        # list ships that can be built on the planet
        query = "SELECT category, shipid, killed, lost" + \
                " FROM users_ships_kills" + \
                "    INNER JOIN db_ships ON (db_ships.id = users_ships_kills.shipid)" + \
                " WHERE userid=" + str(self.userId) + \
                " ORDER BY shipid"
        oRss = oConnExecuteAll(query)

        content = getTemplate(self.request, "s03/fleets-ships-stats")

        count = 0
        kills = 0
        losses = 0
        
        cats = []
        content.setValue("cats", cats)
        
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

        if count == 0: content.Parse("no_ship")
        else: content.Parse("total")
        
        content.setValue("kills", kills)
        content.setValue("losses", losses)

        return self.display(content)
