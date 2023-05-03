# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        #---
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        #---
        
        cat = ToInt(request.GET.get("cat"), 1)
        if cat < 1 or cat > 3: cat = 1
        
        #---
        
        if cat == 2:

            query = "SELECT buildingid, (quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END) AS quantity, disabled" + \
                    " FROM planet_buildings" + \
                    "    INNER JOIN db_buildings ON (planet_buildings.buildingid=db_buildings.id)" + \
                    " WHERE can_be_disabled AND planetid=" + str(self.currentPlanetId)
            rows = dbRows(query)
            
            for row in rows:

                quantity = row['quantity'] - ToInt(request.POST.get("enabled" + str(row['buildingid'])), 0)

                query = "UPDATE planet_buildings SET" + \
                        " disabled=LEAST(quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END, " + str(quantity) + ")" + \
                        "WHERE planetid=" + str(self.currentPlanetId) + " AND buildingid =" + str(row['buildingid'])
                dbQuery(query)
        
        #---
        
        elif cat == 3:
            
            action = request.GET.get("a")
            
            #---
            
            if action == "cancel":
            
                energy_to = ToInt(request.GET.get("to"), 0)
                energy_from = ToInt(request.GET.get("from"), 0)

                if energy_from != 0: query = "DELETE FROM planet_energy_transfer WHERE planetid=" + str(energy_from) + " AND target_planetid=" + str(self.currentPlanetId)
                else: query = "DELETE FROM planet_energy_transfer WHERE planetid=" + str(self.currentPlanetId) + " AND target_planetid=" + str(energy_to)
                dbQuery(query)
            
            #---
            
            elif action == "submit":

                query = "SELECT target_planetid, energy, enabled" + \
                        " FROM planet_energy_transfer" + \
                        " WHERE planetid=" + str(self.currentPlanetId)
                rows = dbRows(query)

                for row in rows:
                    
                    query = ""

                    energy = ToInt(request.POST.get("energy_" + str(row['target_planetid'])), 0)
                    if energy != row['energy']: query = query + "energy = " + str(energy)

                    enabled = request.POST.get("enabled_" + str(row['target_planetid']))
                    if enabled == "1": enabled = True
                    else: enabled = False

                    if enabled != row['enabled']:
                        if query != "": query = query + ","
                        query = query + "enabled=" + str(enabled)

                    if query != "":
                    
                        query = "UPDATE planet_energy_transfer SET " + query + " WHERE planetid=" + str(self.currentPlanetId) + " AND target_planetid=" + str(row['target_planetid'])
                        dbQuery(query)

                        update_planet = True

                g = ToInt(request.POST.get("to_g"), 0)
                s = ToInt(request.POST.get("to_s"), 0)
                p = ToInt(request.POST.get("to_p"), 0)
                energy = ToInt(request.POST.get("energy"), 0)

                if g != 0 and s != 0 and p != 0 and energy > 0:
                
                    query = "INSERT INTO planet_energy_transfer(planetid, target_planetid, energy) VALUES(" + str(self.currentPlanetId) + ", sp_planet(" + str(g) + "," + str(s) + "," + str(p) + ")," + str(energy) + ")"
                    dbQuery(query)

                    update_planet = True

                if update_planet:
                
                    query = "SELECT sp_update_planet(" + str(self.currentPlanetId) + ")"
                    dbQuery(query)
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
    
    def get(self, request, *args, **kwargs):

        #---
        
        self.selectedMenu = "planet"

        self.showHeader = True
        self.headerUrl = '/s03/production/'

        content = getTemplate(request, "s03/production")

        #---
        
        cat = ToInt(request.GET.get("cat"), 1)
        if cat < 1 or cat > 3: cat = 11
                    
        content.setValue("cat", cat)
        
        self.urlExtraParams = "cat=" + str(cat)
        
        #---

        if cat == 1:
            
            #---
            
            query = "SELECT pct_ore, pct_hydrocarbon," + \
                    " workers, workers_for_maintenance, int4(workers / GREATEST(1.0, workers_for_maintenance) * 100) AS production_percent," + \
                    " int4(previous_buildings_dilapidation / 100.0) AS condition," + \
                    " int4(production_percent * 100) AS final_production" + \
                    " FROM vw_planets WHERE id=" + str(self.currentPlanetId)
            planet = dbRow(query)
            
            content.setValue("planet", planet)
            
            #---
            
            query = "SELECT vw_buildings.id, db_buildings.label, db_buildings.description, working_quantity," + \
                    " (vw_buildings.production_ore * working_quantity)::integer AS production_ore, (vw_buildings.production_hydrocarbon * working_quantity)::integer AS production_hydrocarbon, (vw_buildings.energy_production * working_quantity)::integer AS production_energy" + \
                    " FROM vw_buildings" + \
                    "   INNER JOIN db_buildings ON db_buildings.id = vw_buildings.id" + \
                    " WHERE planetid=" + str(self.currentPlanetId) + " AND (vw_buildings.production_ore > 0 OR vw_buildings.production_hydrocarbon > 0 OR vw_buildings.energy_production > 0) AND working_quantity > 0"
            rows = dbRows(query)

            content.setValue("buildings", rows)
            
            totalOre = 0
            totalEnergy = 0
            totalHydrocarbon = 0

            for row in rows:

                totalOre += row['production_ore']
                totalEnergy += row['production_energy']
                totalHydrocarbon += row['production_hydrocarbon']
                
            content.setValue("production_ore", int(totalOre))
            content.setValue("production_energy", int(totalEnergy))
            content.setValue("production_hydrocarbon", int(totalHydrocarbon))

            #---
            
            self.bonuses = []
            content.setValue("bonuses", self.bonuses)

            query = "SELECT commanders.id, commanders.name," + \
                    " (commanders.mod_production_ore - 1) AS mod_production_ore, (commanders.mod_production_hydrocarbon - 1) AS mod_production_hydrocarbon, (commanders.mod_production_energy - 1) AS mod_production_energy" + \
                    " FROM commanders" + \
                    "   INNER JOIN nav_planet ON (commanders.id = nav_planet.commanderid)" + \
                    " WHERE nav_planet.id=" + str(self.currentPlanetId)
            rows = dbRows(query)

            self.displayBonuses(rows, 0)

            query = "SELECT buildingid AS id, label AS name, description," + \
                    " (mod_production_ore * quantity) AS mod_production_ore, (mod_production_hydrocarbon * quantity) AS mod_production_hydrocarbon, (mod_production_energy * quantity) AS mod_production_energy" + \
                    " FROM planet_buildings" + \
                    "    INNER JOIN db_buildings ON (db_buildings.id = planet_buildings.buildingid)" + \
                    " WHERE planetid=" + str(self.currentPlanetId) + " AND (mod_production_ore != 0 OR mod_production_hydrocarbon != 0 OR mod_production_energy != 0)"
            rows = dbRows(query)

            self.displayBonuses(rows, 1)

            query = "SELECT researchid AS id, label AS name, description, level," + \
                    " (level * mod_production_ore) AS mod_production_ore, (level * mod_production_hydrocarbon) AS mod_production_hydrocarbon, (level * mod_production_energy) AS mod_production_energy" + \
                    " FROM researches" + \
                    "   INNER JOIN db_research ON (researches.researchid = db_research.id)" + \
                    " WHERE userid=" + str(self.userId) + " AND (mod_production_ore > 0 OR mod_production_hydrocarbon > 0 OR mod_production_energy > 0) AND level > 0"
            rows = dbRows(query)

            self.displayBonuses(rows, 2)
            
            #---
            
            query = "SELECT int4(COALESCE(sum(effective_energy), 0)) FROM planet_energy_transfer WHERE target_planetid=" + str(self.currentPlanetId)
            energyReceived = dbExecute(query)

            query = "SELECT ore_production, hydrocarbon_production, (energy_production - " + str(energyReceived) + ") AS energy_production FROM nav_planet WHERE id=" + str(self.currentPlanetId)
            row = dbRow(query)

            content.setValue("bonus_production_ore", int(row['ore_production'] - totalOre))
            content.setValue("bonus_production_hydrocarbon", int(row['hydrocarbon_production'] - totalHydrocarbon))
            content.setValue("bonus_production_energy", int(row['energy_production'] - totalEnergy))

            content.setValue("total_production_ore", int(row['ore_production']))
            content.setValue("total_production_hydrocarbon", int(row['hydrocarbon_production']))
            content.setValue("total_production_energy", int(row['energy_production']))

        #---
        
        elif cat == 2:
            
            #---
        
            query = "SELECT buildingid, (quantity - CASE WHEN destroy_datetime IS NULL THEN 0 ELSE 1 END) AS quantity, disabled, energy_consumption, int4(workers*maintenance_factor/100.0) AS maintenance, upkeep," + \
                    " label" + \
                    " FROM planet_buildings" + \
                    "    INNER JOIN db_buildings ON (planet_buildings.buildingid=db_buildings.id)" + \
                    " WHERE can_be_disabled AND quantity > 0 AND planetid=" + str(self.currentPlanetId) + \
                    " ORDER BY buildingid"
            rows = dbRows(query)

            content.setValue("buildings", rows)
            
            for row in rows:
                
                enabled = row['quantity'] - row['disabled']

                row["energy_total"] = round(enabled * row['energy_consumption'])
                row["upkeep_total"] = round(enabled * row['upkeep'])
                row["maintenance_total"] = round(enabled * row['maintenance'])

                row["counts"] = []
                for i in range(0, row['quantity'] + 1):
                
                    data = {}
                    data["count"] = i
                    
                    if i == enabled: data["selected"] = True
                    
                    row["counts"].append(data)

        #---
        
        elif cat == 3:
            
            #---
            
            query = "SELECT energy_receive_antennas, energy_send_antennas FROM nav_planet WHERE id=" + str(self.currentPlanetId)
            planet = dbRow(query)
            
            content.setValue("planet", planet)
            
            max_receive = planet['energy_receive_antennas']
            max_send = planet['energy_send_antennas']
            
            #---
            
            query = "SELECT t.planetid, sp_get_planet_name(" + str(self.userId) + ", n1.id) AS planetname, sp_relation(n1.ownerid," + str(self.userId) + ") AS relation, n1.galaxy, n1.sector, n1.planet, " + \
                    "        t.target_planetid, sp_get_planet_name(" + str(self.userId) + ", n2.id) AS target_planetname, sp_relation(n2.ownerid," + str(self.userId) + ") AS target_relation, n2.galaxy AS target_galaxy, n2.sector AS target_sector, n2.planet AS target_planet, " + \
                    "        t.energy, t.effective_energy, enabled" + \
                    " FROM planet_energy_transfer t" + \
                    "    INNER JOIN nav_planet n1 ON (t.planetid=n1.id)" + \
                    "    INNER JOIN nav_planet n2 ON (t.target_planetid=n2.id)" + \
                    " WHERE planetid=" + str(self.currentPlanetId) + " OR target_planetid=" + str(self.currentPlanetId) + \
                    " ORDER BY not enabled, planetid, target_planetid"
            rows = dbRows(query)

            receiving = 0
            sending_enabled = 0

            sents = []
            content.setValue("sents", sents)
            
            receiveds = []
            content.setValue("receiveds", receiveds)
            
            for row in rows:
            
                item = {}
                
                item["energy"] = row['energy']
                item["effective_energy"] = row['effective_energy']
                
                item["loss"] = self.getPercent(row['energy'] - row['effective_energy'], row['energy'], 1)

                if row['planetid'] == self.currentPlanetId:
                
                    if row['enabled']:
                        sending_enabled = sending_enabled + 1
                        item["enabled"] = True
                        
                    item["planetid"] = row['target_planetid']
                    item["name"] = row['target_planetname']
                    item["rel"] = row['target_relation']
                    item["g"] = row['target_galaxy']
                    item["s"] = row['target_sector']
                    item["p"] = row['target_planet']

                    sents.append(item)
                    
                elif row['enabled']:

                    receiving = receiving + 1

                    item["planetid"] = row['planetid']
                    item["name"] = row['planetname']
                    item["rel"] = row['relation']
                    item["g"] = row['galaxy']
                    item["s"] = row['sector']
                    item["p"] = row['planet']

                    receiveds.append(item)

            content.setValue("antennas_receive_used", receiving)
            content.setValue("antennas_send_used", sending_enabled)

            if max_send == 0: content.Parse("send_no_antenna")
            if max_receive == 0: content.Parse("receive_no_antenna")

            if receiving > 0:
                content.Parse("cant_send_when_receiving")
                max_send = 0

            if sending_enabled > 0:
                content.Parse("cant_receive_when_sending")
                max_receive = 0
            elif receiving == 0 and max_receive > 0:
                content.Parse("receiving_none")

            if max_receive > 0: content.Parse("receive")
            if max_send - len(sents) > 0: content.Parse("send")
            if max_send > 0: content.Parse("submit")
        
        #---

        return self.display(content, request)

    def displayBonuses(self, rows, type):
    
        for row in rows:
        
            item = {}
            self.bonuses.append(item)
            
            item["id"] = row['id']
            item["name"] = row['name']

            item["mod_production_ore"] = round(row['mod_production_ore'] * 100)
            item["mod_production_energy"] = round(row['mod_production_energy'] * 100)
            item["mod_production_hydrocarbon"] = round(row['mod_production_hydrocarbon'] * 100)

            if type == 0:
                item["commander"] = True

            elif type == 1:
                item["building"] = True
                item["description"] = row['description']

            else:
                item["research"] = True
                item["level"] = row['level']
                item["description"] = row['description']
