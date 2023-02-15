# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):
    
    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        self.selected_menu = "planet"
        
        self.showHeader = True
        
        retrieveBuildingsCache()
        retrieveBuildingsReqCache()
        
        Action = request.GET.get("a", "").lower()
        BuildingId = ToInt(request.GET.get("b"), "")
        
        if BuildingId != "":
            BuildingId = BuildingId
        
            if Action == "build":
                self.StartBuilding(BuildingId)
        
            elif Action== "cancel":
                self.CancelBuilding(BuildingId)
    
            elif Action== "destroy":
                self.DestroyBuilding(BuildingId)
        
        y = ToInt(request.GET.get("y"),"")
        scriptname = request.META.get("SCRIPT_NAME")
        
        if y != "":
            request.session["scrollExpire"] = 5/(24*3600) # allow 5 seconds
            request.session["scrollPage"] = scriptname
            request.session["scrolly"] = y
            
            return HttpResponseRedirect(scriptname + "?planet=" + str(self.CurrentPlanet))
        else:
            
            # if scrolly is stored in the session and is still valid, set the scrolly of the displayed page
            if request.session.get("scrolly") != "" and request.session.get("scrollExpire", 0) > 0 and request.session.get("scrollPage") == scriptname:
                self.scrollY = request.session.get("scrolly")
                request.session["scrolly"] = ""
            
            self.RetrievePlanetInfo()
            return self.ListBuildings()

    def RetrievePlanetInfo(self):
        # Retrieve recordset of current planet
        query = "SELECT ore, hydrocarbon, workers-workers_busy, workers_capacity - workers, energy, " + \
                " floor - floor_occupied, space - space_occupied," + \
                " mod_production_ore, mod_production_hydrocarbon, mod_production_energy," + \
                " ore_capacity, hydrocarbon_capacity," + \
                " scientists, scientists_capacity, soldiers, soldiers_capacity, energy_production-energy_consumption" + \
                " FROM vw_planets" + \
                " WHERE id="+str(self.CurrentPlanet)
        oRs = oConnExecute(query)
    
        if oRs == None: return
    
        self.OreBonus = oRs[7]
        self.HydroBonus = oRs[8]
        self.EnergyBonus = oRs[9]
        self.pOre = oRs[0]
        self.pHydrocarbon = oRs[1]
        self.pWorkers = oRs[2]
        self.pVacantWorkers = oRs[3]
        self.pEnergy = oRs[4]
        self.pFloor = oRs[5]
        self.pSpace = oRs[6]
        self.pBonusEnergy = oRs[9]
        self.pOreCapacity = oRs[10]
        self.pHydrocarbonCapacity = oRs[11]
    
        self.pScientists = oRs[12]
        self.pScientistsCapacity = oRs[13]
        self.pSoldiers = oRs[14]
        self.pSoldiersCapacity = oRs[15]
    
        # Retrieve buildings of current planet
        query = "SELECT planetid, buildingid, quantity FROM planet_buildings WHERE quantity > 0 AND planetid=" + str(self.CurrentPlanet)
        oPlanetBuildings = oConnExecute(query)
        
        if not oPlanetBuildings:
            self.buildingsCount = -1
        else:
            self.buildingsArray = oPlanetBuildings
            self.buildingsCount = len(self.buildingsArray)
    
    # check if we already have this building on the planet and return the number of this building on this planet
    def BuildingQuantity(self, BuildingId):
    
        Quantity = 0
    
        for i in self.buildingsArray:
            if BuildingId == i[1]:
                Quantity = int(i[2])
                break
                
        return Quantity
    
    # check if some buildings on the planet requires the presence of the given building
    def HasBuildingThatDependsOn(self, BuildingId):
        ret = False
    
        for i in retrieveBuildingsReqCache():
            if BuildingId == i[1]:
                requiredBuildId = i[0]
    
                if self.BuildingQuantity(requiredBuildId) > 0:
                    ret = True
                    break
                    
        return ret
    
    def HasEnoughWorkersToDestroy(self, BuildingId):
        ret = True
        
        for i in retrieveBuildingsCache():
            if BuildingId == i[0]:
                if i[5]/2 > self.pWorkers:
                    ret = False
                    break
                    
        return ret
    
    def HasEnoughStorageAfterDestruction(self, BuildingId):
        ret = True
    
        # 1/ if we want to destroy a building that increase max population: check that 
        # the population is less than the limit after the building destruction
        # 2/ if the building produces energy, check that there will be enough energy after
        # the building destruction
        # 3/ if the building increases the capacity of ore or hydrocarbon, check that there is not
        # too much ore/hydrocarbon
        for i in retrieveBuildingsCache():
            if BuildingId == i[0]:
                if i[1] > 0 and self.pVacantWorkers < i[1]:
                    ret = False
                    break
    
                # check if scientists/soldiers are lost
                if self.pScientists > self.pScientistsCapacity-i[6]:
                    ret = False
                    break
    
                if self.pSoldiers > self.pSoldiersCapacity-i[7]:
                    ret = False
                    break
    
                # check if a storage building is destroyed
                if self.pOre > self.pOreCapacity-i[3]:
                    ret = False
                    break
    
                if self.pHydrocarbon > self.pHydrocarbonCapacity-i[4]:
                    ret = False
                    break
                    
        return ret

    def getBuildingMaintenanceWorkers(self, BuildingId):
        ret = 0
    
        for i in retrieveBuildingsCache():
            if BuildingId == i[0]:
                ret = i[11]
                break
                    
        return ret
    
    # List all the available buildings
    def ListBuildings(self):
    
        # count number of buildings under construction
        oRs = oConnExecute("SELECT int4(count(*)) FROM planet_buildings_pending WHERE planetid=" + str(self.CurrentPlanet) + " LIMIT 1")
        underConstructionCount = oRs[0]
    
        # list buildings that can be built on the planet
        query = "SELECT id, category, cost_prestige, cost_ore, cost_hydrocarbon, cost_energy, cost_credits, workers, floor, space," + \
                "construction_maximum, quantity, build_status, construction_time, destroyable, '', production_ore, production_hydrocarbon, energy_production, buildings_requirements_met, destruction_time," + \
                "upkeep, energy_consumption, buildable" + \
                " FROM vw_buildings" + \
                " WHERE planetid=" + str(self.CurrentPlanet) + " AND ((buildable AND research_requirements_met) or quantity > 0)"
    
        oRss = oConnExecute(query)
        content = GetTemplate(self.request, "s03/buildings")
    
        content.AssignValue("planetid", str(self.CurrentPlanet))
    
        cat_id = -1
        lastCategory = -1
            
        categories = []
        index = 1
        for oRs in oRss:
            # if can be built or has some already built, display it
            if oRs[19] or oRs[11] > 0:
        
                BuildingId = oRs[0]
        
                CatId = oRs[1]
        
                if CatId != lastCategory:
                    category = {'id': CatId, 'buildings':[]}
                    categories.append(category)
                    lastCategory = CatId
                    
                building = {}
                building["id"] = BuildingId
                building["name"] = getBuildingLabel(oRs[0])
        
                building["ore"] = oRs[3]
                building["hydrocarbon"] = oRs[4]
                building["energy"] = oRs[5]
                building["credits"] = oRs[6]
                building["workers"] = oRs[7]
                building["prestige"] = oRs[2]
        
                building["floor"] = oRs[8]
                building["space"] = oRs[9]
                building["time"] = oRs[13]
                building["description"] = getBuildingDescription(oRs[0])
        
                OreProd= oRs[16]
                HydroProd= oRs[17]
                EnergyProd= oRs[18]
        
                building["ore_prod"] = int(OreProd)
                building["hydro_prod"] = int(HydroProd)
                building["energy_prod"] = int(EnergyProd)
                building["ore_modifier"] = int(OreProd*(self.OreBonus-100)/100)
                building["hydro_modifier"] = int(HydroProd*(self.HydroBonus-100)/100)
                building["energy_modifier"] = int(EnergyProd*(self.EnergyBonus-100)/100)
        
                if OreProd != 0 or HydroProd != 0 or EnergyProd != 0:
                    if self.OreBonus < 100 and OreProd != 0:
                        building["tipprod_ore_malus"] = True
                    else:
                        building["tipprod_ore_bonus"] = True
                    
                    building["tipprod_ore"] = True

                    if self.HydroBonus < 100 and HydroProd != 0:
                        building["tipprod.hydro.malus"] = True
                    else:
                        building["tipprod.hydro.bonus"] = True
                    
                    building["tipprod.hydro"] = True

                    if self.EnergyBonus < 100 and EnergyProd != 0:
                        building["tipprod.energy.malus"] = True
                    else:
                        building["tipprod.energy.bonus"] = True
                    
                    building["tipprod.energy"] = True
                    building["tipprod"] = True
                
                maximum = oRs[10]
                quantity = oRs[11]
        
                building["quantity"] = quantity
        
                status = oRs[12]
        
                building["remainingtime"] = ""
                building["nextdestroytime"] = ""
        
                if status:
                    if status < 0: status = 0
        
                    building["remainingtime"] = status
                    building["underconstruction"] = True
                    building["isbuilding"] = True
        
                elif not oRs[23]:
                    building["limitreached"] = True
                elif (quantity > 0) and (quantity >= maximum):
                    if quantity == 1:
                        building["built"] = True
                    else:
                        building["limitreached"] = True
                    
                elif not oRs[19]:
        
                    building["buildings_required"] = True
        
                else:
                    notenoughspace = False
                    notenoughresources = False
        
                    if oRs[8] > self.pFloor:
                        building["not_enough_floor"] = True
                        notenoughspace = True
                        
                    if oRs[9] > self.pSpace:
                        building["not_enough_space"] = True
                        notenoughspace = True
                        
                    if oRs[2] > 0 and oRs[2] > self.oPlayerInfo["prestige_points"]:
                        building["not_enough_prestige"] = True
                        notenoughresources = True
                        
                    if oRs[3] > 0 and oRs[3] > self.pOre:
                        building["not_enough_ore"] = True
                        notenoughresources = True
                        
                    if oRs[4] > 0 and oRs[4] > self.pHydrocarbon:
                        building["not_enough_hydrocarbon"] = True
                        notenoughresources = True
                    
                    if oRs[5] > 0 and oRs[5] > self.pEnergy:
                        building["not_enough_energy"] = True
                        notenoughresources = True
                        
                    if oRs[7] > 0 and oRs[7] > self.pWorkers:
                        building["not_enough_workers"] = True
                        notenoughresources = True
                    
                    if notenoughspace: building["not_enough.space"] = True
                    if notenoughresources: building["not_enough.resources"] = True
        
                    if notenoughspace or notenoughresources:
                        building["not_enough"] = True
                    else:
                        building["build"] = True

                if (quantity > 0) and oRs[14]:
        
                    if oRs[20]:
                        building["nextdestroytime"] = oRs[20]
                        building["next_destruction_in"] = True
                        building["isdestroying"] = True
                    elif not self.HasEnoughWorkersToDestroy(BuildingId):
                        building["workers_required"] = True
                    elif self.HasBuildingThatDependsOn(BuildingId):
                        building["required"] = True
                    elif not self.HasEnoughStorageAfterDestruction(BuildingId):
                        building["capacity"] = True
                    else:
                        building["destroy"] = True
                    
                else:
                    building["empty"] = True
                    
                building["index"] = index
                index = index + 1
        
                building["workers_for_maintenance"] = self.getBuildingMaintenanceWorkers(BuildingId)
                building["upkeep"] = oRs[21]
                building["upkeep_energy"] = oRs[22]
        
                category['buildings'].append(building)
    
        content.AssignValue("categories", categories)
        
        return self.Display(content)
    
    def StartBuilding(self, BuildingId):
        oRs = connExecuteRetry("SELECT sp_start_building(" + str(self.UserId) + "," + str(self.CurrentPlanet) + ", " + str(BuildingId) + ", false)")
        
    def CancelBuilding(self, BuildingId):
        result = oConnRow("SELECT sp_cancel_building(" + str(self.UserId) + "," + str(self.CurrentPlanet) + ", " + str(BuildingId) + ") AS result")
        print(result)
    
    def DestroyBuilding(self, BuildingId):
        connExecuteRetryNoRecords("SELECT sp_destroy_building(" + str(self.UserId) + "," + str(self.CurrentPlanet) + "," + str(BuildingId) + ")")
