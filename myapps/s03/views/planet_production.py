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
        
        self.selectedMenu = "planet"

        self.showHeader = True
        self.headerUrl = '/s03/planet-production/'

        content = getTemplate(request, "s03/production")

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
