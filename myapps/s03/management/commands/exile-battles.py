# -*- coding: utf_8 -*-

import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from myapps.s03.battle import *

from myapps.s03.views.utils import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        connectDB()
        start = timezone.now()
        while timezone.now() - start < timedelta(seconds=55):
            oRss = oConnExecuteAll("SELECT id, COALESCE(sp_get_user(ownerid), ''), galaxy, sector, planet FROM nav_planet WHERE next_battle <= now() LIMIT 1;")
            if oRss:
                for oRs in oRss:
                    planetid = oRs[0]
                    data = "planet:{owner:\"" + str(oRs[1]) + "\",g:" + str(oRs[2]) + ",s:" + str(oRs[3]) + ",p:" + str(oRs[4]) + "}"
                    Rounds = 25
                    
                    # retrieve opponents relationships
                    queryFriends = "SELECT f1.ownerid, f2.ownerid, sp_relation(f1.ownerid, f2.ownerid)" +\
                                    " FROM (SELECT ownerid, bool_or(attackonsight) AS attackonsight FROM fleets WHERE planetid=" + str(planetid) + " AND engaged GROUP BY ownerid) as f1, (SELECT ownerid, bool_or(attackonsight) AS attackonsight FROM fleets WHERE planetid=" + str(planetid) + " AND engaged GROUP BY ownerid) as f2" +\
                                    " WHERE f1.ownerid > f2.ownerid AND (sp_relation(f1.ownerid, f2.ownerid) >= 0 OR (sp_relation(f1.ownerid, f2.ownerid) = -1 AND NOT f1.attackonsight AND NOT f2.attackonsight) );"
                    friendsArray = oConnExecuteAll(queryFriends)
                    
                    # create the battlefield object
                    battle = TBattle()
                    
                    query = "SELECT fleets.ownerid, fleets.id, db_ships.id, hull, shield, handling, weapon_ammo, weapon_power, weapon_tracking_speed, weapon_turrets, quantity, dest_planetid, fleets.mod_shield, fleets.mod_handling, fleets.mod_tracking_speed, fleets.mod_damage, attackonsight," +\
                            " weapon_dmg_em, weapon_dmg_explosive, weapon_dmg_kinetic, weapon_dmg_thermal," +\
                            " resist_em, resist_explosive, resist_kinetic, resist_thermal, tech" +\
                            " FROM (fleets INNER JOIN fleets_ships ON (fleetid = id))" +\
                            "    INNER JOIN db_ships ON (fleets_ships.shipid = db_ships.id)" +\
                            " WHERE fleets.planetid=" + str(planetid) + " AND engaged" +\
                            " ORDER BY fleets.speed DESC, random();"
                    oFleets = oConnExecuteAll(query)
                    
                    # fill the battlefield with the fleets
                    for oFleet in oFleets:
                        if oFleet[11] == None:
                            battle.AddShips(oFleet[0], oFleet[1], oFleet[2], oFleet[3], oFleet[4], oFleet[5], oFleet[6], oFleet[8], oFleet[9], \
                                            {'EM': oFleet[17], 'Explosive': oFleet[18], 'Kinetic': oFleet[19], 'Thermal': oFleet[20]}, \
                                            {'Hull': 100.0, 'Shield': oFleet[12], 'Handling': oFleet[13], 'Tracking_speed': oFleet[14], 'Damage': oFleet[15]}, \
                                            {'EM': oFleet[21], 'Explosive': oFleet[22], 'Kinetic': oFleet[23], 'Thermal': oFleet[24]}, \
                                            oFleet[10], True or oFleet[16], oFleet[25])
                        else:
                            # if the fleet is fleeing, divide the handling of the fleet by 1, its weapon_tracking_speed by 2 and reduce number of rounds that can occur
                            battle.AddShips(oFleet[0], oFleet[1], oFleet[2], oFleet[3], oFleet[4], oFleet[5], oFleet[6], oFleet[8], oFleet[9], \
                                            {'EM': oFleet[17], 'Explosive': oFleet[18], 'Kinetic': oFleet[19], 'Thermal': oFleet[20]}, \
                                            {'Hull': 100.0, 'Shield': oFleet[12], 'Handling': oFleet[13] / 1, 'Tracking_speed': oFleet[14] / 2, 'Damage': oFleet[15]}, \
                                            {'EM': oFleet[21], 'Explosive': oFleet[22], 'Kinetic': oFleet[23], 'Thermal': oFleet[24]}, \
                                            oFleet[10], True or oFleet[16], oFleet[25])

                    # set the relations between players
                    for friend in friendsArray:
                        battle.SetRelation(friend[0], friend[1])
                    
                    # let's the battle begin !
                    battle.BeginFight()
                    while Rounds > 1 and battle.NextRound(1):
                        Rounds = Rounds - 1
                    battle.EndFight()
                    
                    # retrieve number of rounds
                    Rounds = battle.FRounds
                    
                    # create a new battle in database
                    query = "SELECT sp_create_battle(" + str(planetid) + "," + str(Rounds) + ")"
                    oBattleRS = oConnExecute(query)
                    BattleId = oBattleRS[0]
                    
                    # store players relationships
                    for friend in friendsArray:
                        if friend[0] > friend[1]:
                            p1 = friend[1]
                            p2 = friend[0]
                        else:
                            p1 = friend[0]
                            p2 = friend[1]
                        
                        query = "INSERT INTO battles_relations VALUES(" + str(BattleId) + "," + str(p1) + "," + str(p2) + "," + str(friend[2]) + ")"
                        oConnDoQuery(query)
                    
                    # write battle result
                    shipsDestroyed = 0
                    lastOwner = -1
                    lastFleetId = ""
                    lastBattleFleetId = ""
                    
                    for grp in battle.FGroupList:
                        
                        # create an entry for each shipid with before/after
                        query = "INSERT INTO battles_ships(battleid, owner_id, owner_name, fleet_id, fleet_name, shipid, before, after, killed, won, damages, attacked, hull, shield, handling, damage, tracking)" +\
                                " VALUES(" + str(BattleId) + "," + str(grp.FOwner.FId) + ", (SELECT username FROM users WHERE id=" + str(grp.FOwner.FId) + " LIMIT 1), " + str(grp.FFleetid) + ", (SELECT name FROM fleets WHERE id=" + str(grp.FFleetid) + " LIMIT 1)," + str(grp.FId) + "," + str(grp.FBefore) + "," + str(grp.FBefore - grp.FShipLoss) + "," + str(grp.FKilled) + "," + str(grp.FOwner.FIsWinner) + "," + str(grp.FDamages) + "," + "(SELECT attackonsight FROM fleets WHERE id=" + str(grp.FFleetid) + " LIMIT 1)," + str(grp.FHull) + "," + str(grp.FShield) + "," + str(grp.FHandling) + "," + str(grp.FWeaponDamages) + "," + str(grp.FWeapon_tracking_speed) + ")"
                        oConnDoQuery(query)
                        
                        # new way of saving battle
                        
                        if grp.FFleetid != lastFleetId:
                            # add a fleet in the battle report
                            query = "SELECT sp_add_battle_fleet(" + str(BattleId) + "," + str(grp.FOwner.FId) + "," + str(grp.FFleetid) + "," + str(int(grp.Fmod_shield)) + "," + str(int(grp.Fmod_handling)) + "," + str(int(grp.Fmod_tracking_speed)) + "," + str(int(grp.Fmod_damage)) + "," + "(SELECT attackonsight FROM fleets WHERE id=" + str(grp.FFleetid) + " LIMIT 1), " + str(grp.FOwner.FIsWinner) + ")"
                            oFleets = oConnExecute(query)
                            
                            lastFleetid = grp.FFleetid
                            lastBattleFleetId = oFleets[0]
                        
                        query = "INSERT INTO battles_fleets_ships(fleetid, shipid, before, after, killed, damages)" +\
                                " VALUES(" + str(lastBattleFleetId) + "," + str(grp.FId) + "," + str(grp.FBefore) + "," + str(grp.FBefore - grp.FShipLoss) + "," + str(grp.FKilled) + "," + str(grp.FDamages) + ")"
                        oConnDoQuery(query)
                        
                        for kill in grp.FKillList:
                            query = "INSERT INTO battles_fleets_ships_kills(fleetid, shipid, destroyed_shipid, count)" +\
                                    " VALUES(" + str(lastBattleFleetId) + "," + str(grp.FId) + "," + str(kill["DestroyedGroup"].FId) + "," + str(kill["Count"]) + ")"
                            oConnDoQuery(query)
                            
                            # count number of ships killed
                            if kill["Count"] > 0:
                                query = "INSERT INTO users_ships_kills(userid, shipid, killed)" +\
                                        " VALUES(" + str(grp.FOwner.FId) + "," + str(kill["DestroyedGroup"].FId) + "," + str(kill["Count"]) + ")"
                                oConnDoQuery(query)
                                
                        shipsDestroyed = shipsDestroyed + grp.FShipLoss
                        
                        # count number of ships the owner lost
                        if grp.FShipLoss > 0:
                            query = "SELECT sp_destroy_ships(" + str(grp.FFleetid) + "," + str(grp.FId) + "," + str(grp.FShipLoss) + ")"
                            oConnDoQuery(query)
                            
                            query = "INSERT INTO users_ships_kills(userid, shipid, lost)" +\
                                    " VALUES(" + str(grp.FOwner.FId) + "," + str(grp.FId) + "," + str(grp.FShipLoss) + ")"
                            oConnDoQuery(query)
                        
                        if lastOwner != grp.FOwner.FId:
                            if grp.FOwner.FIsWinner:
                                battlesubtype = 1
                            else:
                                battlesubtype = 0
                            
                            query = "SELECT ownerid FROM reports WHERE ownerid=" + str(grp.FOwner.FId) + " AND type=2 AND subtype=" + str(battlesubtype) + " AND battleid=" + str(BattleId)
                            reportRs = oConnExecute(query)
                            if reportRs == None:
                                query = "INSERT INTO reports(ownerid, type, subtype, battleid, planetid, data)" +\
                                        " VALUES(" + str(grp.FOwner.FId) + ",2," + str(battlesubtype) + "," + str(BattleId) + "," + str(planetid) + ",'{" + str(data) + ",battleid:" + str(BattleId) + ",ownerid:" + str(grp.FOwner.FId) + "}'" + ")"
                                oConnDoQuery(query)
                            
                            lastOwner = grp.FOwner.FId
                    
                    query = "UPDATE nav_planet SET next_battle = null WHERE id=" + str(planetid)
                    oConnDoQuery(query)
                    
                    query = "UPDATE fleets SET engaged=false WHERE engaged AND action <> 0 AND planetid=" + str(planetid)
                    oConnDoQuery(query)
                    
                    if shipsDestroyed > 0:
                        oConnDoQuery("SELECT sp_check_battle(" + str(planetid) + ")")
                    else:
                        query = "UPDATE fleets SET engaged=false, action=4, action_end_time=now()"
                        if Rounds > 5: query = query + ", idle_since=now()"
                        query = query & " WHERE engaged AND action=0 AND planetid=" + str(planetid)
                        oConnDoQuery(query)
                        
            time.sleep(0.5)
