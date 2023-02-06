# -*- coding: utf-8 -*-

import math

from functools import cmp_to_key
from random import *

from django.utils import timezone

class TBattle:
    
    def __init__(self):
        self.FRounds = 0
        self.FPlayers = []
        self.FLastLog = None
        self.FKillList = []
        self.FGroupList = []
        self.FCombatLog = []
        self.FBattleEnd = None
        self.FBattleStart = None
        self.FCombatLogEnabled = True
        self.FEnemyShipsRemaining = 0

    def AddShips(self, Ownerid, Fleetid, Shipid, Hull, Shield, Handling, weapon_ammo, weapon_tracking_speed, weapon_turrets, weapon_damage, Mods, Resistances, Quantity, FireAtWill, Tech):
        P = self.GetPlayer(Ownerid)
        
        P.AddShip(Fleetid, Shipid, Hull, Shield, Handling, weapon_ammo, weapon_tracking_speed, weapon_turrets, weapon_damage, Mods, Resistances, Quantity, FireAtWill, Tech)
        
    def BeginFight(self):
        self.FBattleStart = timezone.now()

        self.FRounds = 0

        for player in self.FPlayers:
            player.Init()

        # sort the group list to know who shoot first
        self.FGroupList = sorted(self.FGroupList, key=cmp_to_key(SortGroupsByFirstShooter))
        
    def NextRound(self, MaxRounds):
        Result = self.CanFight()
        if not Result: return Result

        # rounds
        for R in range(1, MaxRounds + 1):
            self.NewRound()

            AmmoRemaining = False
            while not AmmoRemaining:

                # Make every group fire
                for group in self.FGroupList:
                    if group.Fight2():
                        AmmoRemaining = True

            if not self.CanFight():
                Result = False
                break
         
        return Result
        
    def EndFight(self):
        # battle is over
        for player in self.FPlayers:
            player.Over()

        # Sort groups by owner
        self.FGroupList = sorted(self.FGroupList, key=cmp_to_key(SortGroupsByOwnerId))

        for group in self.FGroupList:
            for kill in group.FKillList:
                self.FKillList.append(kill)

        self.FBattleEnd = timezone.now()
    
    # Return if a fight can happen
    # no fight can happen if everyone is friend
    def CanFight(self):
        for player in self.FPlayers:
            if player.FShipCount > 0:
                for enemy in player.FEnemies:
                    if enemy.FShipCount > 0:
                        return True

        return False
        
    # Return whether it hits or not
    def Fire(self, Ship, Target, ChanceToHit, Damage):

        Result = False
        
        X = random()
        if X > ChanceToHit:
            Ship.FMiss += 1
            return False # Missed !

        Ship.FHit += 1

        Result = True

        if Target.FUnitShield > 0: Damage = Damage * 0.75

        if Damage > Target.FUnitShield:
            Ship.FDamages = Ship.FDamages + Target.FUnitShield
            Damage = Damage - Target.FUnitShield

            Damage = Damage * Ship.Fmult_damage

            Target.FUnitShield = 0

            if Damage > Target.FUnitHull:
                Ship.FDamages = Ship.FDamages + Target.FUnitHull
                Target.FUnitHull = 0
            else:
                Ship.FDamages = Ship.FDamages + Damage
                Target.FUnitHull = Target.FUnitHull - Damage

            if Target.FUnitHull == 0:
                self.ShipDestroyed(Target, Ship)
        else:
            Target.FUnitShield = Target.FUnitShield - Damage
            Ship.FDamages = Ship.FDamages + Damage

    def GetDestroyedShips(self, index):
        Result = self.FKillList[index]

    def GetDestroyedShipsCount(self):
        Result = Length(FKillList)

    def GetPlayer(self, Id):
        # retrieve combatant if already exists
        for player in self.FPlayers:
            if player.FId == Id:
                return player

        # Create a new combatant
        Result = TPlayer(self, Id)

        self.FPlayers.append(Result)

        # Add it as an enemy for other combatant
        for player in self.FPlayers:
            if player != Result:
                player.FEnemies.append(Result)
                Result.FEnemies.append(player)
        
        return Result

    def NewRound(self):
        self.FRounds += 1

        # Notice each opponent that a new round begin
        for player in self.FPlayers:
            player.NewRound()

    def SetRelation(self, Ownerid1, Ownerid2):
        P1 = self.GetPlayer(Ownerid1)
        P2 = self.GetPlayer(Ownerid2)

        P1.FEnemies.remove(P2)
        P2.FEnemies.remove(P1)

    def ShipDestroyed(self, Target, ByGroup):
        Target.ShipDestroyed()
        ByGroup.EnemyShipDestroyed(Target)

# sort the groups by "first shooter" order
def SortGroupsByFirstShooter(Ship1, Ship2):
    if Ship1.FTech > Ship2.FTech:
        return 1
    else:
        if Ship1.FTech < Ship2.FTech:
            return -1
        else:
            if Ship1.FWeapon_ammo > Ship2.FWeapon_ammo:
                return 1
            else:
                if Ship1.FWeapon_ammo < Ship2.FWeapon_ammo:
                    return -1
                else:
                    return 0

def SortGroupsByOwnerId(Ship1, Ship2):
    if Ship1.FOwner.FId < Ship2.FOwner.FId:
        return -1
    else:
        if Ship1.FOwner.FId > Ship2.FOwner.FId:
            return 1
        else:
            return 0
 
def GetChanceToHit(WeaponTracking, TargetHandling, Tech, TargetTech):
    if TargetHandling == 1:
        return 1.0

    ChanceHit = WeaponTracking / 1000
    ChanceDodge = TargetHandling / 1000
    ChanceEvade = (TargetHandling - WeaponTracking) / 1000

    if ChanceHit > 1:
        ChanceDodge = ChanceDodge - (ChanceHit-1)
        ChanceHit = 1

    while Tech < TargetTech:
        ChanceHit = ChanceHit * 0.85
        Tech += 1

    while Tech > TargetTech:
        ChanceHit = ChanceHit * 1.10
        Tech -= 1

    if ChanceDodge < 0: ChanceDodge = 0
    if ChanceDodge > 0.90: ChanceDodge = 0.90

    if ChanceEvade < 0: ChanceEvade = 0
    if ChanceEvade > 0.90: ChanceEvade = 0.90

    Result =  ChanceHit * (1-ChanceDodge) * (1-ChanceEvade)

    if Result > 1: Result = 1
    if Result == 0: Result = 0.0000001
    
    return Result

# Compute damage according to resistance
def CompDamage(Damage, Resistance):

    Result = Damage

    # Additional damage recution
    # damage = 1
    # resist = 20 (1/2 = 50% reduc)
    Protection = Resistance/10
    if Protection > 0:
        if Result < Protection: Result = Result*(Result/Protection)

    return max(Result * (1 - Resistance/100), 0)

def GetWeaponDamage(WeaponDamage, ShipResistance):
    if (WeaponDamage["EM"] == 0) and (WeaponDamage["Explosive"] == 0) and (WeaponDamage["Kinetic"] == 0) and (WeaponDamage["Thermal"] == 0):
        return 0

    if (ShipResistance["EM"] == 0) and (ShipResistance["Explosive"] == 0) and (ShipResistance["Kinetic"] == 0) and (ShipResistance["Thermal"] == 0):
        return WeaponDamage["EM"] + WeaponDamage["Explosive"] + WeaponDamage["Kinetic"] + WeaponDamage["Thermal"]

    return CompDamage(WeaponDamage["EM"], ShipResistance["EM"]) +\
            CompDamage(WeaponDamage["Explosive"], ShipResistance["Explosive"]) +\
            CompDamage(WeaponDamage["Kinetic"], ShipResistance["Kinetic"]) +\
            CompDamage(WeaponDamage["Thermal"], ShipResistance["Thermal"])

def AverageHitsToKill(WeaponDamage, WeaponTrackingSpeed, TargetHull, TargetShield, TargetHandling, TargetResistance, Tech, TargetTech):
    total_hp = TargetHull + TargetShield
    damage = Min(GetWeaponDamage(WeaponDamage, TargetResistance), total_hp)

    Result = total_hp / ( Max(damage, 0.00001) * GetChanceToHit(WeaponTrackingSpeed, TargetHandling, Tech, TargetTech) )

    if Result == 0: Result = MaxInt

def AverageHitsOn(WeaponDamage, WeaponTrackingSpeed, TargetHull, TargetShield, TargetHandling, TargetResistance, Tech, TargetTech):
    total_hp = TargetHull + TargetShield
    damage = min(GetWeaponDamage(WeaponDamage, TargetResistance), total_hp)

    return max(damage, 0.00001) * GetChanceToHit(WeaponTrackingSpeed, TargetHandling, Tech, TargetTech)

class TPlayer:

    def AddShip(self, Fleetid, Shipid, Hull, Shield, Handling, weapon_ammo, weapon_tracking_speed, weapon_turrets, weapon_damage, Mods, Resistances, Quantity, FireAtWill, Tech):
        self.FAggressive = self.FAggressive or FireAtWill

        Grp = TShipsGroup(self, Fleetid, Shipid, Hull, Shield, Handling,\
                                weapon_ammo, weapon_tracking_speed, weapon_turrets, weapon_damage,\
                                Mods, Resistances,\
                                Quantity, Tech)
        self.FGroups.append(Grp)
        self.FBattle.FGroupList.append(Grp)

    def __init__(self, Battle, AId):
        self.FAggressive = False

        self.FBattle = Battle
        self.FId = AId

        self.FEnemies = []
        self.FEnemyGroups = []

        self.FShipCount = 0

        self.FGroups = []

        self.FIsWinner = False

        self.FShipActivations = 0
        self.FSkipEvery = 0

    def Destroy(self):
        self.FEnemies.Free
        self.FEnemyGroups.Free

        for group in self.FGroups:
            group.Free
        self.FGroups.Free

    def Fight2(self):
        Result = False

        for group in self.FGroups:
            if group.Fight2():
                Result = True

    def Init(self):
        # Remove enemies that are not aggressive if we are not aggressive
        if not self.FAggressive:
            for Enemy in self.FEnemies:
                if not Enemy.self.FAggressive:
                    self.FEnemies.remove(Enemy)

        # Initialize the list of enemy groups
        for Enemy in self.FEnemies:
            P = Enemy

            for Group in P.FGroups:
                self.FEnemyGroups.append(Group)

        shuffle(self.FEnemyGroups)

    # Call NewRound for every ship group
    def NewRound(self):
        for Group in self.FGroups:
            Group.NewRound()

    # Called when battle is over
    def Over(self):
        self.FIsWinner = False

        # Check if there are any enemy left
        for Grp in self.FEnemyGroups:
            if Grp.FBefore > Grp.FShipLoss:
                return

        # Check that some ships remain to be declared "winner"
        for Grp in self.FGroups:
            if Grp.FBefore > Grp.FShipLoss:
                self.FIsWinner = True
                return

    def ShipDestroyed(self, Target):
        self.FShipCount -= 1

class TShipsGroup:

    def __init__(self, Owner, Fleetid, ShipId, Hull, Shield, Handling, Weapon_ammo, Weapon_tracking_speed, Weapon_turrets, Weapon_damage, Mods, Resistances, Quantity, Tech):
        
        self.FHit = 0
        self.FDamages = 0
        self.FKillList = []
        self.FCurrentTarget = None
        self.FChangeTargetIn = 0
        
        self.FOwner = Owner
        self.FId = ShipId

        self.FTech = Tech

        self.FRemainingShips = Quantity

        self.FOwner.FShipCount += Quantity

        self.FShipLoss = 0

        self.FKilled = 0
        self.FMiss = 0

        # Assign ship stats
        self.FFleetid = Fleetid
        self.FId = ShipId
        self.FHull = Hull

        self.FResistances = Resistances
        self.FWeapon_damage = Weapon_damage

        self.FBaseHandling = Handling
        self.FBaseHull = Hull
        self.FBaseShield = Shield
        self.FBaseWeapon_tracking_speed = Weapon_tracking_speed

        # Assign raw bonus
        self.Fmod_hull = Mods["Hull"]
        self.Fmod_shield = Mods["Shield"]
        self.Fmod_handling = Mods["Handling"]
        self.Fmod_tracking_speed = Mods["Tracking_speed"]
        self.Fmod_damage = Mods["Damage"]

        # compute the effective multiplicator for each bonus
        self.Fmult_hull = self.Fmod_hull / 100
        self.Fmult_shield = self.Fmod_shield / 100
        self.Fmult_handling = (100 + (self.Fmod_handling - 100) / 10) / 100
        self.Fmult_tracking_speed = (100 + (self.Fmod_tracking_speed - 100) / 10) / 100
        
        if self.Fmod_damage > 100: self.Fmult_damage = (100 + (self.Fmod_damage - 100) / 10) / 100
        else: self.Fmult_damage = self.Fmod_damage / 100

        # Compute ship protection : shield < 100% can decrease it
        self.FHull = Hull*self.Fmult_hull
        self.FShield = Shield*self.Fmult_shield          # compute the value of the shield
        self.FHandling = int(Handling*self.Fmult_handling)# Max(Handling*Fmult_handling, 1)
        if self.FHandling <= 1: self.FHandling = 1

        self.FWeaponDamages = (Weapon_damage["EM"]+Weapon_damage["Explosive"]+Weapon_damage["Kinetic"]+Weapon_damage["Thermal"]) * Weapon_turrets * math.log10(1+Weapon_tracking_speed)

        self.FWeapon_ammo = Weapon_ammo
        self.FWeapon_tracking_speed = int(Weapon_tracking_speed*self.Fmult_tracking_speed)
        self.FWeapon_turrets = Weapon_turrets

        self.FPrecision = Weapon_tracking_speed

        # Compute the type of target we want for this group
        self.FBestHandlingTarget = int(self.FPrecision * 1.5)

        self.FHasPriorityTargets = True

        self.FUnitHull = self.FHull
        self.FUnitShield = self.FShield

        self.FBefore = Quantity

    def Destroy(self):
        pass
    
    def PrioritySort(self, Ship1, Ship2):
        Sc1 = AverageHitsOn(self.FWeapon_damage, self.FBaseWeapon_tracking_speed, Ship1.FBaseHull, Ship1.FBaseShield, Ship1.FBaseHandling, Ship1.FResistances, self.FTech, Ship1.FTech)
        Sc2 = AverageHitsOn(self.FWeapon_damage, self.FBaseWeapon_tracking_speed, Ship2.FBaseHull, Ship2.FBaseShield, Ship2.FBaseHandling, Ship2.FResistances, self.FTech, Ship2.FTech)

        if Sc1 > Sc2:
            return -1
        else:
            if Sc1 < Sc2:
                return 1
            else:
                return 0

    def FindTargetList(self):
        TargetList = []

        # Retrieve the possible targets from the list of enemy ships

        for Grp in self.FOwner.FEnemyGroups:
            if (Grp.FWeaponDamages > 0) and (Grp.FRemainingShips > 0):
                TargetList.append(Grp)

        # If no prioritary targets, fill the secondary targets
        if len(TargetList) == 0:
            self.FHasPriorityTargets = False

            for Grp in self.FOwner.FEnemyGroups:
                if (Grp.FRemainingShips > 0):
                    TargetList.append(Grp)

        if len(TargetList) > 0:
            # Sort the list by priority
            shuffle(TargetList)
            TargetList = sorted(TargetList, key=cmp_to_key(self.PrioritySort))

            Result = TargetList
        else:
            Result = None

        return Result
        
    def FindTarget(self):
        TargetList = []

        # Retrieve the possible targets from the list of enemy ships

        for Grp in self.FOwner.FEnemyGroups:
            if (Grp.FWeaponDamages > 0) and (Grp.FRemainingShips > 0):
                TargetList.append(Grp)

        # If no prioritary targets, fill the secondary targets
        if len(TargetList) == 0:
            self.FHasPriorityTargets = False

            for Grp in self.FOwner.FEnemyGroups:
                if (Grp.FRemainingShips > 0):
                    TargetList.append(Grp)

        if len(TargetList) > 0:
            # Sort the list by priority
            shuffle(TargetList)
            TargetList = sorted(TargetList, key=cmp_to_key(self.PrioritySort))

            Result = TargetList[0]
        else:
            Result = None

        return Result

    def GetTarget(self):
        if (self.FChangeTargetIn <= 0) or ((self.FCurrentTarget != None) and (self.FCurrentTarget.FRemainingShips <= 0)):
            self.FCurrentTarget = None

        if self.FCurrentTarget == None:
            self.FCurrentTarget = self.FindTarget()

            self.FChangeTargetIn = 10
        
        return self.FCurrentTarget

    def NewRound(self):
        self.FRemainingAmmo = self.FWeapon_ammo
        self.FShipsForRound = self.FRemainingShips

    def GetLoss(self):
        Result = self.FShipLoss

    def EnemyShipDestroyed(self, Group):
        self.FChangeTargetIn -= 1
        self.FKilled += 1

        for Item in self.FKillList:
            if Item["DestroyedGroup"] == Group:
                Item["Count"] += 1
                return

        Item = {}
        Item["Group"] = self
        Item["DestroyedGroup"] = Group
        Item["Count"] = 1
        self.FKillList.append(Item)

    def Fight2(self):
        Result = False
        if self.FRemainingAmmo == 0: return False

        I = self.FShipsForRound * min(self.FRemainingAmmo, self.FWeapon_turrets)

        # remove number of ammo used
        if self.FRemainingAmmo >= self.FWeapon_turrets:
            self.FRemainingAmmo -= self.FWeapon_turrets
        else:
            self.FRemainingAmmo = 0

        LastTarget = None
        Hit = 0
        Dmg = 0

        while I > 0:
            Target = self.GetTarget()

            if Target == None: break  # Target = nil when no more targets
            if (LastTarget != Target):
                Hit = GetChanceToHit(self.FWeapon_tracking_speed, Target.FHandling, self.FTech, Target.FTech)
                Dmg = GetWeaponDamage(self.FWeapon_damage, Target.FResistances)
                LastTarget = Target

            Result = True

            self.FOwner.FBattle.Fire(self, Target, Hit, Dmg)

            I -= 1
        
        return Result

    def GetDamages(self):
        return round(min(self.FDamages, 2000000000))

    def GetKill(self, index):
        Result = self.FKillList[index]

    def ShipDestroyed(self):
        self.FRemainingShips -= 1
        self.FShipLoss += 1

        # Remove ship from owner shiplist
        self.FOwner.ShipDestroyed(self)

        if self.FRemainingShips > 0:
            self.FUnitHull = self.FHull
            self.FUnitShield = self.FShield
