# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "fleets.standby"

        return self.ListStandby()

    # List the fleets owned by the player
    def ListStandby(self):
        content = getTemplate(self.request, "s03/fleets-standby")

        # list the ships
        query = "SELECT nav_planet.id, nav_planet.name, nav_planet.galaxy, nav_planet.sector, nav_planet.planet, shipid, quantity" + \
                " FROM planet_ships" + \
                "    INNER JOIN nav_planet ON (planet_ships.planetid = nav_planet.id)" + \
                " WHERE nav_planet.ownerid =" + str(self.userId) + \
                " ORDER BY nav_planet.id, shipid"
        oRss = oConnExecuteAll(query)

        if oRss == None:
            content.Parse("noships")
        else:
            lastplanetid = -1

            list = []
            content.setValue("planets", list)
            for oRs in oRss:
                
                if oRs[0] != lastplanetid:
                    planet = { "ships":[] }
                    list.append(planet)
                    
                    lastplanetid = oRs[0]

                    planet["planetid"] = oRs[0]
                    planet["planetname"] = oRs[1]
                    planet["g"] = oRs[2]
                    planet["s"] = oRs[3]
                    planet["p"] = oRs[4]
                    
                item = {}
                planet["ships"].append(item)
                
                item["ship"] = getShipLabel(oRs[5])
                item["quantity"] = oRs[6]

        return self.display(content)
