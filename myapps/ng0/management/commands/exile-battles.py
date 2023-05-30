# -*- coding: utf_8 -*-

import time
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from myapps.s03.battle import *

from myapps.s03.views._utils import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        #---
        
        dbConnect()
        
        #---
        
        start = timezone.now()
        while timezone.now() - start < timedelta(seconds=55):
            
            #---
            rows = dbRows("SELECT id, COALESCE(sp_get_user(ownerid), '') AS username, galaxy, sector, planet FROM nav_planet WHERE next_battle <= now() LIMIT 1;")
            if rows:
                for row in rows:
                
                    #---
                    
                    planetId = row['id']
                    data = "planet:{owner:\"" + str(row['username']) + "\",g:" + str(row['galaxy']) + ",s:" + str(row['sector']) + ",p:" + str(row['planet']) + "}"
                    
                    #---
                    
                    battle = TBattle()
                    
                    Rounds = 25
                    
                    query = "SELECT sp_create_battle(" + str(planetId) + "," + str(Rounds) + ")"
                    battleId = dbExecute(query)
                    
                    #---
                    
                    query = "SELECT fleets.ownerid, fleets.id, db_ships.id AS shipid, hull, shield, handling, weapon_ammo, weapon_power, weapon_tracking_speed, weapon_turrets, quantity, dest_planetid, fleets.mod_shield, fleets.mod_handling, fleets.mod_tracking_speed, fleets.mod_damage, attackonsight," +\
                            " weapon_dmg_em, weapon_dmg_explosive, weapon_dmg_kinetic, weapon_dmg_thermal," +\
                            " resist_em, resist_explosive, resist_kinetic, resist_thermal, tech" +\
                            " FROM (fleets INNER JOIN fleets_ships ON (fleetid = id))" +\
                            "    INNER JOIN db_ships ON (fleets_ships.shipid = db_ships.id)" +\
                            " WHERE fleets.planetId=" + str(planetId) + " AND engaged" +\
                            " ORDER BY fleets.speed DESC, random();"
                    rows = dbRows(query)
                    
                    for row in rows:
                        if row['dest_planetid'] == None:
                        
                            battle.AddShips(row['ownerid'], row['id'], row['shipid'], row['hull'], row['shield'], row['handling'], row['weapon_ammo'], row['weapon_tracking_speed'], row['weapon_turrets'], \
                                            {'EM': row['weapon_dmg_em'], 'Explosive': row['weapon_dmg_explosive'], 'Kinetic': row['weapon_dmg_kinetic'], 'Thermal': row['weapon_dmg_thermal']}, \
                                            {'Hull': 100.0, 'Shield': row['mod_shield'], 'Handling': row['mod_handling'], 'Tracking_speed': row['mod_tracking_speed'], 'Damage': row['mod_damage']}, \
                                            {'EM': row['resist_em'], 'Explosive': row['resist_explosive'], 'Kinetic': row['resist_kinetic'], 'Thermal': row['resist_thermal']}, \
                                            row['quantity'], True or row['attackonsight'], row['tech'])
                        else:

                            battle.AddShips(row['ownerid'], row['id'], row['shipid'], row['hull'], row['shield'], row['handling'], row['weapon_ammo'], row['weapon_tracking_speed'], row['weapon_turrets'], \
                                            {'EM': row['weapon_dmg_em'], 'Explosive': row['weapon_dmg_explosive'], 'Kinetic': row['weapon_dmg_kinetic'], 'Thermal': row['weapon_dmg_thermal']}, \
                                            {'Hull': 100.0, 'Shield': row['mod_shield'], 'Handling': row['mod_handling'], 'Tracking_speed': row['mod_tracking_speed'] / 2, 'Damage': row['mod_damage']}, \
                                            {'EM': row['resist_em'], 'Explosive': row['resist_explosive'], 'Kinetic': row['resist_kinetic'], 'Thermal': row['resist_thermal']}, \
                                            row['quantity'], True or row['attackonsight'], row['tech'])

                    #---
                    
                    query = "SELECT f1.ownerid AS p1, f2.ownerid AS p2, sp_relation(f1.ownerid, f2.ownerid) AS relation" +\
                            " FROM (SELECT ownerid, bool_or(attackonsight) AS attackonsight FROM fleets WHERE planetId=" + str(planetId) + " AND engaged GROUP BY ownerid) as f1, (SELECT ownerid, bool_or(attackonsight) AS attackonsight FROM fleets WHERE planetId=" + str(planetId) + " AND engaged GROUP BY ownerid) as f2" +\
                            " WHERE f1.ownerid > f2.ownerid AND (sp_relation(f1.ownerid, f2.ownerid) >= 0 OR (sp_relation(f1.ownerid, f2.ownerid) = -1 AND NOT f1.attackonsight AND NOT f2.attackonsight) );"
                    rows = dbRows(query)
                    
                    for row in rows:
                    
                        battle.SetRelation(row['p1'], row['p2'])
                        
                        if row['p1'] > row['p2']:
                            p1 = row['p2']
                            p2 = row['p1']
                        else:
                            p1 = row['p1']
                            p2 = row['p2']
                        
                        query = "INSERT INTO battles_relations VALUES(" + str(battleId) + "," + str(p1) + "," + str(p2) + "," + str(row['relation']) + ")"
                        dbQuery(query)
                    
                    #---
                    
                    battle.BeginFight()
                    
                    while Rounds > 0 and battle.NextRound(1):
                        Rounds = Rounds - 1
                        
                    battle.EndFight()
                    
                    Rounds = battle.FRounds
                   
                    #---
                    
                    shipsDestroyed = 0
                    lastOwner = -1
                    lastFleetId = ""
                    lastBattleFleetId = ""
                    
                    for grp in battle.FGroupList:
                        
                        query = "INSERT INTO battles_ships(battleid, owner_id, owner_name, fleet_id, fleet_name, shipid, before, after, killed, won, damages, attacked, hull, shield, handling, damage, tracking)" +\
                                " VALUES(" + str(battleId) + "," + str(grp.FOwner.FId) + ", (SELECT username FROM users WHERE id=" + str(grp.FOwner.FId) + " LIMIT 1), " + str(grp.FFleetid) + ", (SELECT name FROM fleets WHERE id=" + str(grp.FFleetid) + " LIMIT 1)," + str(grp.FId) + "," + str(grp.FBefore) + "," + str(grp.FBefore - grp.FShipLoss) + "," + str(grp.FKilled) + "," + str(grp.FOwner.FIsWinner) + "," + str(grp.FDamages) + "," + "(SELECT attackonsight FROM fleets WHERE id=" + str(grp.FFleetid) + " LIMIT 1)," + str(grp.FHull) + "," + str(grp.FShield) + "," + str(grp.FHandling) + "," + str(grp.FWeaponDamages) + "," + str(grp.FWeapon_tracking_speed) + ")"
                        dbQuery(query)
                        
                        if grp.FFleetid != lastFleetId:

                            query = "SELECT sp_add_battle_fleet(" + str(battleId) + "," + str(grp.FOwner.FId) + "," + str(grp.FFleetid) + "," + str(int(grp.Fmod_shield)) + "," + str(int(grp.Fmod_handling)) + "," + str(int(grp.Fmod_tracking_speed)) + "," + str(int(grp.Fmod_damage)) + "," + "(SELECT attackonsight FROM fleets WHERE id=" + str(grp.FFleetid) + " LIMIT 1), " + str(grp.FOwner.FIsWinner) + ")"
                            lastBattleFleetId = dbExecute(query)                            
                            lastFleetid = grp.FFleetid
                        
                        query = "INSERT INTO battles_fleets_ships(fleetid, shipid, before, after, killed, damages)" +\
                                " VALUES(" + str(lastBattleFleetId) + "," + str(grp.FId) + "," + str(grp.FBefore) + "," + str(grp.FBefore - grp.FShipLoss) + "," + str(grp.FKilled) + "," + str(grp.FDamages) + ")"
                        dbQuery(query)
                        
                        for kill in grp.FKillList:
                        
                            query = "INSERT INTO battles_fleets_ships_kills(fleetid, shipid, destroyed_shipid, count)" +\
                                    " VALUES(" + str(lastBattleFleetId) + "," + str(grp.FId) + "," + str(kill["DestroyedGroup"].FId) + "," + str(kill["Count"]) + ")"
                            dbQuery(query)
                            
                            if kill["Count"] > 0:
                            
                                query = "INSERT INTO users_ships_kills(userid, shipid, killed)" +\
                                        " VALUES(" + str(grp.FOwner.FId) + "," + str(kill["DestroyedGroup"].FId) + "," + str(kill["Count"]) + ")"
                                dbQuery(query)
                                
                        shipsDestroyed = shipsDestroyed + grp.FShipLoss
                        
                        if grp.FShipLoss > 0:
                        
                            query = "SELECT sp_destroy_ships(" + str(grp.FFleetid) + "," + str(grp.FId) + "," + str(grp.FShipLoss) + ")"
                            dbQuery(query)
                            
                            query = "INSERT INTO users_ships_kills(userid, shipid, lost)" +\
                                    " VALUES(" + str(grp.FOwner.FId) + "," + str(grp.FId) + "," + str(grp.FShipLoss) + ")"
                            dbQuery(query)
                        
                        if lastOwner != grp.FOwner.FId:
                        
                            if grp.FOwner.FIsWinner: battlesubtype = 1
                            else: battlesubtype = 0
                            
                            query = "SELECT ownerid FROM reports WHERE ownerid=" + str(grp.FOwner.FId) + " AND type=2 AND subtype=" + str(battlesubtype) + " AND battleid=" + str(battleId)
                            row = dbRow(query)
                            
                            if row == None:
                            
                                query = "INSERT INTO reports(ownerid, type, subtype, battleid, planetId, data)" +\
                                        " VALUES(" + str(grp.FOwner.FId) + ",2," + str(battlesubtype) + "," + str(battleId) + "," + str(planetId) + ",'{" + str(data) + ",battleid:" + str(battleId) + ",ownerid:" + str(grp.FOwner.FId) + "}'" + ")"
                                dbQuery(query)
                            
                            lastOwner = grp.FOwner.FId
                    
                    #---
                    
                    query = "UPDATE nav_planet SET next_battle = null WHERE id=" + str(planetId)
                    dbQuery(query)
                    
                    query = "UPDATE fleets SET engaged=false WHERE engaged AND action <> 0 AND planetId=" + str(planetId)
                    dbQuery(query)
                    
                    #---
                    
                    if shipsDestroyed > 0:
                    
                        dbQuery("SELECT sp_check_battle(" + str(planetId) + ")")
                        
                    else:
                    
                        query = "UPDATE fleets SET engaged=false, action=4, action_end_time=now()"
                        if Rounds > 5: query = query + ", idle_since=now()"
                        query = query + " WHERE engaged AND action=0 AND planetId=" + str(planetId)
                        dbQuery(query)
                        
            #---     
            
            time.sleep(0.5)
