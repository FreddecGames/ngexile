# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "planets"

        return self.ListPlanets()

    def ListPlanets(self):

        content = GetTemplate(self.request, "s03/planets")

        #
        # Setup column ordering
        #
        col = ToInt(self.request.GET.get("col"), 0)

        if col < 0 or col > 5: col = 0

        reversed = False
        if col == 0:
            orderby = "id"
        elif col == 1:
            orderby = "upper(name)"
        elif col == 2:
            orderby = "ore_production"
        elif col == 3:
            orderby = "hydrocarbon_production"
        elif col == 4:
            orderby = "energy_consumption/(1.0+energy_production)"
        elif col == 5:
            orderby = "mood"

        if self.request.GET.get("r", "") != "":
            reversed = not reversed
        else:
            content.Parse("r" + str(col))
        content.AssignValue('col', col)

        if reversed: orderby = orderby + " DESC"
        orderby = orderby + ", upper(name)"

        query = "SELECT t.id, name, galaxy, sector, planet," + \
                "ore, ore_production, ore_capacity," + \
                "hydrocarbon, hydrocarbon_production, hydrocarbon_capacity," + \
                "workers-workers_busy, workers_capacity," + \
                "energy_production - energy_consumption, energy_capacity," + \
                "floor, floor_occupied," + \
                "space, space_occupied," + \
                "commanderid, (SELECT name FROM commanders WHERE id = t.commanderid) AS commandername," + \
                "mod_production_ore, mod_production_hydrocarbon, workers, t.soldiers, soldiers_capacity," + \
                "t.scientists, scientists_capacity, workers_for_maintenance, planet_floor, mood," + \
                "energy, mod_production_energy, upkeep, energy_consumption," + \
                " (SELECT int4(COALESCE(sum(scientists), 0)) FROM planet_training_pending WHERE planetid=t.id) AS scientists_training," + \
                " (SELECT int4(COALESCE(sum(soldiers), 0)) FROM planet_training_pending WHERE planetid=t.id) AS soldiers_training," + \
                " credits_production, credits_random_production, production_prestige" + \
                " FROM vw_planets AS t" + \
                " WHERE planet_floor > 0 AND planet_space > 0 AND ownerid="+str(self.UserId)+ \
                " ORDER BY "+orderby

        oRss = oConnExecuteAll(query)
        
        list = []
        content.AssignValue("page_planets", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            mood_delta = 0

            item["planet_img"] = self.planetimg(oRs[0], oRs[29])

            item["planet_id"] = oRs[0]
            item["planet_name"] = oRs[1]

            item["g"] = oRs[2]
            item["s"] = oRs[3]
            item["p"] = oRs[4]

                # ore
            item["ore"] = oRs[5]
            item["ore_production"] = oRs[6]
            item["ore_capacity"] = oRs[7]

            # compute ore level : ore / capacity
            ore_level = self.getpercent(oRs[5], oRs[7], 10)

            if ore_level >= 90:
                item["high_ore"] = True
            elif ore_level >= 70:
                item["medium_ore"] = True
            else:
                item["normal_ore"] = True

            # hydrocarbon
            item["hydrocarbon"] = oRs[8]
            item["hydrocarbon_production"] = oRs[9]
            item["hydrocarbon_capacity"] = oRs[10]

            # compute hydrocarbon level : hydrocarbon / capacity
            hydrocarbon_level = self.getpercent(oRs[8], oRs[10], 10)

            if hydrocarbon_level >= 90:
                item["high_hydrocarbon"] = True
            elif hydrocarbon_level >= 70:
                item["medium_hydrocarbon"] = True
            else:
                item["normal_hydrocarbon"] = True

            # energy
            item["energy"] = oRs[31]
            item["energy_production"] = oRs[13]
            item["energy_capacity"] = oRs[14]

            # compute energy level : energy / capacity
            energy_level = self.getpercent(oRs[31], oRs[14], 10)

            item["normal_energy"] = True

            credits = oRs[37] + (oRs[38] / 2)

            item["credits"] = int(credits)
            if credits < 0:
                item["credits_minus"] = True
            else:
                item["credits_plus"] = True

            item["prestige"] = oRs[39]

            if oRs[13] < 0:
                item["negative_energy_production"] = True
            elif oRs[32] >= 0 and oRs[23] >= oRs[28]:
                item["normal_energy_production"] = True
            else:
                item["medium_energy_production"] = True

            # workers
            item["workers"] = oRs[23]
            item["workers_idle"] = oRs[11]
            item["workers_capacity"] = oRs[12]

            # soldiers
            item["soldiers"] = oRs[24]
            item["soldiers_capacity"] = oRs[25]
            item["soldiers_training"] = oRs[36]

            # scientists
            item["scientists"] = oRs[26]
            item["scientists_capacity"] = oRs[27]
            item["scientists_training"] = oRs[35]

            if oRs[23] < oRs[28]: item["workers_low"] = True

            if oRs[24]*250 < oRs[23]+oRs[26]: item["soldiers_low"] = True

            # mood
            if oRs[30] > 100:
                item["mood"] = 100
            else:
                item["mood"] = oRs[30]

            moodlevel = round(oRs[30] / 10) * 10
            if moodlevel > 100: moodlevel = 100

            item["mood_level"] = moodlevel

            if (oRs[19]): mood_delta = mood_delta + 1

            if oRs[24]*250 >= oRs[23]+oRs[26]:
                mood_delta = mood_delta + 2
            else:
                mood_delta = mood_delta - 1

            item["mood_delta"] = mood_delta
            if mood_delta > 0:
                item["mood_plus"] = True
            else:
                item["mood_minus"] = True

            # planet stats
            item["floor_capacity"] = oRs[15]
            item["floor_occupied"] = oRs[16]

            item["space_capacity"] = oRs[17]
            item["space_occupied"] = oRs[18]

            if oRs[19]:
                item["commander_id"] = oRs[19]
                item["commander_name"] = oRs[20]
                item["commander"] = True
            else:
                item["nocommander"] = True

            if oRs[21] >= 0 and oRs[23] >= oRs[28]:
                item["normal_ore_production"] = True
            else:
                item["medium_ore_production"] = True

            if oRs[22] >= 0 and oRs[23] >= oRs[28]:
                item["normal_hydrocarbon_production"] = True
            else:
                item["medium_hydrocarbon_production"] = True

            item["upkeep_credits"] = oRs[33]
            item["upkeep_workers"] = oRs[28]
            item["upkeep_soldiers"] = int((oRs[23]+oRs[26]) / 250)

            if oRs[0] == self.CurrentPlanet: item["highlight"] = True

        return self.Display(content)
