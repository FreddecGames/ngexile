# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

def FormatBattle(view, battleid, creator, pointofview, ispubliclink):

    # Retrieve/assign battle info
    query = "SELECT time, planetid, name, galaxy, sector, planet, rounds," + \
            "EXISTS(SELECT 1 FROM battles_ships WHERE battleid=" + str(battleid) + " AND owner_id=" + str(creator) + " AND won LIMIT 1), MD5(key||"+str(creator)+")," + \
            "EXISTS(SELECT 1 FROM battles_ships WHERE battleid=" + str(battleid) + " AND owner_id=" + str(creator) + " AND damages > 0 LIMIT 1) AS see_details" + \
            " FROM battles" + \
            "    INNER JOIN nav_planet ON (planetid=nav_planet.id)" + \
            " WHERE battles.id = " + str(battleid)
    oRs = oConnExecute(query)

    if oRs == None: return

    content = GetTemplate(view.request, "battle")

    content.AssignValue("battleid", battleid)
    content.AssignValue("userid", creator)
    content.AssignValue("key", oRs[8])

    if not ispubliclink:
        # link for the freely viewable report of this battle
        content.AssignValue("baseurl", view.request.META.get("HTTP_HOST"))
        content.Parse("publiclink")

    content.AssignValue("time", oRs[0])
    content.AssignValue("planetid", oRs[1])
    content.AssignValue("planet", oRs[2])
    content.AssignValue("g", oRs[3])
    content.AssignValue("s", oRs[4])
    content.AssignValue("p", oRs[5])
    content.AssignValue("rounds", oRs[6])

    rounds = oRs[6]
    hasWon = oRs[7]
    showEnemyDetails = oRs[9] or hasWon or rounds > 1

    query = "SELECT fleet_id, shipid, destroyed_shipid, sum(count)" + \
            " FROM battles_fleets" + \
            "    INNER JOIN battles_fleets_ships_kills ON (battles_fleets.id=fleetid)" + \
            " WHERE battleid=" + str(battleid) + \
            " GROUP BY fleet_id, shipid, destroyed_shipid" + \
            " ORDER BY sum(count) DESC"
    killsArray = oConnExecuteAll(query)

    query = "SELECT owner_name, fleet_name, shipid, shipcategory, shiplabel, count, lost, killed, won, relation1, owner_id , relation2, fleet_id, attacked, mod_shield, mod_handling, mod_tracking_speed, mod_damage, alliancetag" + \
            " FROM sp_get_battle_result(" + str(battleid) + "," + str(creator) + "," + str(pointofview) + ")"

    oRss = oConnExecuteAll(query)

    if oRss:
        opponents = []
        content.AssignValue("opponents", opponents)
        
        lastFleetId = -1
        lastCategory = -1
        lastPlayerName = ""
        
        for oRs in oRss:
            
            playerName = oRs[0]
            if playerName != lastPlayerName:
                opponent = { 'fleets':[], "count":0,  "lost":0, "killed":0, "after":0 }
                opponents.append(opponent)
                
                opponent["name"] = playerName
                opponent["view"] = oRs[10]
                
                if ispubliclink: opponent["public"] = True
                
                if oRs[13]: opponent["attack"] = True
                else: opponent["defend"] = True
                
                if oRs[18]:
                    opponent["alliancetag"] = oRs[18]
                    opponent["alliance"] = True
                    
                if oRs[11] == rSelf: opponent["self"] = True
                elif oRs[11] == rAlliance: opponent["ally"] = True
                elif oRs[11] == rFriend: opponent["friend"] = True
                else: opponent["enemy"] = True
                
                if oRs[8]: opponent["won"] = True
                
                lastPlayerName = playerName
            
            fleetId = oRs[12]
            if fleetId != lastFleetId:
                fleet = { 'ships':[], "count":0,  "lost":0, "killed":0, "after":0 }
                opponent['fleets'].append(fleet)
                
                fleet["name"] = oRs[1]
                    
                if oRs[11] == rSelf: fleet["self"] = True
                elif oRs[11] == rAlliance: fleet["ally"] = True
                elif oRs[11] == rFriend: fleet["friend"] = True
                else: fleet["enemy"] = True
                
                if not showEnemyDetails and oRs[9] < rFriend:
                    fleet["mod_shield"] = "?"
                    fleet["mod_handling"] = "?"
                    fleet["mod_tracking_speed"] = "?"
                    fleet["mod_damage"] = "?"
                else:
                    fleet["mod_shield"] = oRs[14]
                    fleet["mod_handling"] = oRs[15]
                    fleet["mod_tracking_speed"] = oRs[16]
                    fleet["mod_damage"] = oRs[17]
                
                lastFleetId = fleetId
            
            if showEnemyDetails or oRs[9] >= rFriend:
                
                # if not a friend and there was no more than a fixed number of rounds, display ships by category and not their name
                if not hasWon and rounds <= 1 and oRs[9] < rFriend:
                    
                    category = oRs[3]
                    if category != lastCategory:
                        ship = { "ships":0, "lost":0, "killed":0, "after":0 }
                        fleet['ships'].append(ship)
                        
                        ship["category" + str(category)] = True
                        
                        lastCategory = category
                
                    ship["ships"] += oRs[5]
                    ship["lost"] += oRs[6]
                    ship["killed"] += oRs[7]
                    ship["after"] += oRs[5]-oRs[6]
                    
                else:
                    ship = { 'kills':[] }
                    fleet['ships'].append(ship)
                    
                    ship["label"] = oRs[4]
                    ship["ships"] = oRs[5]
                    ship["lost"] = oRs[6]
                    ship["killed"] = oRs[7]
                    ship["after"] = oRs[5]-oRs[6]
                    
                    killed = 0
                    for i in killsArray:
                        if oRs[12] == i[0] and oRs[2] == i[1]:
                            kill = {}
                            ship['kills'].append(kill)
                            
                            kill["killed_name"] = getShipLabel(i[2])
                            kill["killed_count"] = i[3]
                            
                            killed = killed + 1 # count how many different ships were destroyed
        
                    if killed == 0: ship["killed_zero"] = True
                    if killed > 1: ship["killed_total"] = True
        
                fleet["count"] += oRs[5]
                fleet["lost"] += oRs[6]
                fleet["killed"] += oRs[7]
                fleet["after"] += oRs[5]-oRs[6]
        
                opponent["count"] += oRs[5]
                opponent["lost"] += oRs[6]
                opponent["killed"] += oRs[7]
                opponent["after"] += oRs[5]-oRs[6]
                
    return content
