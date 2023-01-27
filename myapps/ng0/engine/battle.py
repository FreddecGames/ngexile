import random

from functools import cmp_to_key


def getChanceToHit(tracking, handling):

    if handling == 1: return 1.0

    chanceHit = tracking / 1000
    chanceDodge = handling / 1000
    chanceEvade = (handling - tracking) / 1000

    if chanceHit > 1:
        chanceDodge = chanceDodge - (chanceHit - 1)
        chanceHit = 1

    if chanceDodge < 0: chanceDodge = 0
    if chanceDodge > 0.90: chanceDodge = 0.90

    if chanceEvade < 0: chanceEvade = 0
    if chanceEvade > 0.90: chanceEvade = 0.90

    result = chanceHit * (1 - chanceDodge) * (1 - chanceEvade)

    if result > 1: result = 1
    if result == 0: result = 0.0000001
    
    return result

def getWeaponDamage(damages, resistances):

    if damages['em'] == 0 and damages['explosive'] == 0 and damages['kinetic'] == 0 and damages['thermal'] == 0:
        return 0

    if resistances['em'] == 0 and resistances['explosive'] == 0 and resistances['kinetic'] == 0 and resistances['thermal'] == 0:
        return damages['em'] + damages['explosive'] + damages['kinetic'] + damages['thermal']

    return computeDamage(damages['em'], resistances['em']) + \
           computeDamage(damages['explosive'], resistances['explosive']) + \
           computeDamage(damages['kinetic'], resistances['kinetic']) + \
           computeDamage(damages['thermal'], resistances['thermal'])

def computeDamage(damage, resistance):

    result = damage

    protection = resistance / 10
    if protection > 0:
        if result < protection:
            result = result * (result / protection)

    return max(result * (1 - resistance / 100), 0)


class CBattleShipGroup:
    
    def __init__(self, ownerId, fleetId, shipId, hull, shield, handling, tracking, turrets, damages, resistances, count):
        
        self.killList = []
        self.enemyGroupList = []
        
        self.ownerId = ownerId
        self.fleetId = fleetId
        self.shipId = shipId
        self.hull = hull
        self.shield = shield
        self.handling = handling
        self.tracking = tracking
        self.turrets = turrets
        self.damages = damages
        self.resistances = resistances
        self.count = count
        
        self.remainingCount = self.count
        
        self.changeTargetIn = 0
        self.currentTarget = None
        
        self.currentHull = self.hull
        self.currentShield = self.shield
        
    def fight(self):
        
        chance = 0
        damage = 0
        
        lastTarget = None
        
        shots = self.remainingCount * self.turrets
        while shots > 0:
            
            target = self.getTarget()
            if target == None: break
            
            if lastTarget != target:
            
                chance = getChanceToHit(self.tracking, target.handling)
                damage = getWeaponDamage(self.damages, target.resistances)
                
                lastTarget = target
            
            self.doFire(target, chance, damage)
            
            shots -= 1
            
    def getTarget(self):
    
        if self.changeTargetIn <= 0 or (self.currentTarget != None and self.currentTarget.remainingCount <= 0):
            self.currentTarget = None

        if self.currentTarget == None:
        
            self.currentTarget = self.findTarget()
            self.changeTargetIn = 10
        
        return self.currentTarget

    def findTarget(self):
    
        targetList = []

        for enemyGroup in self.enemyGroupList:
            if enemyGroup.remainingCount > 0:
                targetList.append(enemyGroup)

        if len(targetList) > 0:
            random.shuffle(targetList)
            targetList = sorted(targetList, key = cmp_to_key(self.sortTargetByPriority))
            return targetList[0]

        return None
        
    def sortTargetByPriority(self, ship1, ship2):
    
        sc1 = AverageHitsOn(self.damages, self.tracking, ship1.hull, ship1.shield, ship1.handling, ship1.resistances)
        sc2 = AverageHitsOn(self.damages, self.tracking, ship2.hull, ship2.shield, ship2.handling, ship2.resistances)

        if sc1 > sc2: return -1
        else:
            if sc1 < sc2: return 1
            else: return 0

    def doFire(self, target, chance, damage):
        
        dice = random.random()
        if dice > chance:
            return
        
        if target.currentShield > 0: damage = damage * 0.75
        
        if damage > target.currentShield:
            target.currentShield = 0
        
            damage = damage - target.currentShield
            
            if damage > target.currentHull:
                target.currentHull = 0
                
                target.shipDestroyed()
                self.makeKill(target)
                
            else:
                target.currentHull -= damage
            
        else:        
            target.currentShield -= damage
    
    def shipDestroyed(self):
    
        self.remainingCount -= 1
        if self.remainingCount > 0:
        
            self.currentHull = self.hull
            self.currentShield = self.shield
    
    def makeKill(self, target):
    
        self.changeTargetIn -= 1
        
        for kill in self.killList:
            if kill['shipId'] == target.shipId:
                kill['count'] += 1
                return
        
        self.killList.append({ 'shipId':target.shipId, 'count':1 })

    
def sortGroupsByFirstShooter(groupShip1, groupShip2):

    if groupShip1.turrets > groupShip2.turrets: return 1
    else:
        if groupShip1.turrets < groupShip2.turrets: return -1
        else: return 0


class CBattle:
    
    def __init__(self):
    
        self.shipGroupList = []
    
    def addShipGroup(self, ownerId, fleetId, shipId, hull, shield, handling, tracking, turrets, damages, resistances, count):
        
        shipGroup = CBattleShipGroup(ownerId, fleetId, shipId, hull, shield, handling, tracking, turrets, damages, resistances, count)
        self.shipGroupList.append(shipGroup)
        
        for enemyGroup in self.shipGroupList:
            if enemyGroup.ownerId != shipGroup.ownerId:
            
                enemyGroup.enemyGroupList.append(shipGroup)
                shipGroup.enemyGroupList.append(enemyGroup)

    def beginFight(self):
        
        self.shipGroupList = sorted(self.shipGroupList, key = cmp_to_key(sortGroupsByFirstShooter))
        
    def doRound(self):
    
        if not self.canFight(): return False
        
        for shipGroup in self.shipGroupList:
            shipGroup.fight()
        
        return True
        
    def canFight(self):
        
        for shipGroup in self.shipGroupList:
            if shipGroup.remainingCount > 0:
                for enemyGroup in shipGroup.enemyGroupList:
                    if enemyGroup.remainingCount > 0:
                        return True
        
        return False
    