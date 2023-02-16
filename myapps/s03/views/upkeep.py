# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "upkeep"

        return self.displayUpkeep()

    def displayUpkeep(self):

        content = getTemplate(self.request, "s03/upkeep")

        hours = 24 - timezone.now().hour

        query = "SELECT scientists,soldiers,planets,ships_signature,ships_in_position_signature,ships_parked_signature," + \
                " cost_planets2,cost_scientists,cost_soldiers,cost_ships,cost_ships_in_position,cost_ships_parked," + \
                " int4(upkeep_scientists + scientists*cost_scientists/24*"+str(hours)+"),"+ \
                " int4(upkeep_soldiers + soldiers*cost_soldiers/24*"+str(hours)+"),"+ \
                " int4(upkeep_planets + cost_planets2/24*"+str(hours)+"),"+ \
                " int4(upkeep_ships + ships_signature*cost_ships/24*"+str(hours)+"),"+ \
                " int4(upkeep_ships_in_position + ships_in_position_signature*cost_ships_in_position/24*"+str(hours)+"),"+ \
                " int4(upkeep_ships_parked + ships_parked_signature*cost_ships_parked/24*"+str(hours)+"),"+ \
                " commanders, commanders_salary, cost_commanders, upkeep_commanders + int4(commanders_salary*cost_commanders/24*"+str(hours)+")" + \
                " FROM vw_players_upkeep" + \
                " WHERE userid=" + str(self.userId)
        oRs = oConnExecute(query)

        content.setValue("commanders_quantity", oRs[18])
        content.setValue("commanders_salary", oRs[19])
        content.setValue("commanders_cost", oRs[20])
        content.setValue("commanders_estimated_cost", int(oRs[21]))

        content.setValue("scientists_quantity", oRs[0])
        content.setValue("soldiers_quantity", oRs[1])
        content.setValue("planets_quantity", oRs[2])
        content.setValue("ships_signature", oRs[3])
        content.setValue("ships_in_position_signature", oRs[4])
        content.setValue("ships_parked_signature", oRs[5])

        content.setValue("planets_cost", int(oRs[6]))
        content.setValue("scientists_cost", oRs[7])
        content.setValue("soldiers_cost", oRs[8])
        content.setValue("ships_cost", oRs[9])
        content.setValue("ships_in_position_cost", oRs[10])
        content.setValue("ships_parked_cost", oRs[11])

        content.setValue("scientists_estimated_cost", oRs[12])
        content.setValue("soldiers_estimated_cost", oRs[13])
        content.setValue("planets_estimated_cost", oRs[14])
        content.setValue("ships_estimated_cost", oRs[15])
        content.setValue("ships_in_position_estimated_cost", oRs[16])
        content.setValue("ships_parked_estimated_cost", oRs[17])

        content.setValue("total_estimation", int(oRs[12] + oRs[13] + oRs[14] + oRs[15] + oRs[16] + oRs[17] + oRs[21]))

        return self.display(content)
