# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from myapps.s03.lib.exile import *
from myapps.s03.lib.template import *

from myapps.s03.views.cache import *

class GlobalView(ExileMixin, View):

    CurrentPlanet = None
    CurrentGalaxyId = None
    CurrentSectorId = None
    scrollY = 0 # how much will be scrolled in vertical after the page is loaded
    showHeader = False
    url_extra_params = ""
    pageTerminated = False
    displayAlliancePlanetName = True
    pagelogged = False
    selected_menu = ""
    
    def pre_dispatch(self, request, *args, **kwargs):
        
        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not request.session.get(sUser):
            return HttpResponseRedirect("/") # Redirect to home page

        request.session["details"] = ""
        
        # Check that this session is still valid
        response = self.CheckSessionValidity()
        if response: return response
        
        # Check for the planet querystring parameter and if the current planet belongs to the player
        response = self.CheckCurrentPlanetValidity()
        if response: return response
        
        '''
        referer = self.request.META.get("HTTP_REFERER", "")
        
        if referer != "":
        
            # extract the website part from the referer url
            posslash = referer[8:].find("/")
            if posslash > 0:
                websitename = referer[8:posslash-8]
            else:
                websitename = referer[8:]
        
            if not "exileng.com" in referer.lower() and not referer.lower() in request.META.get("LOCAL_ADDR", "") and not "viewtopic" in referer.lower() and not "forum" in referer.lower():
                oConnExecute("SELECT sp_log_referer("+str(self.UserId)+","+dosql(referer) + ")")
        '''
        
    def hasRight(self, right):
        if self.oAllianceRights == None:
            return True
        else:
            return self.oAllianceRights["leader"] or self.oAllianceRights[right]
    
    def getPlanetName(self, relation, radar_strength, ownerName, planetName):
        if relation == rSelf:
            return planetName if planetName else ""
        elif relation == rAlliance:
            if self.displayAlliancePlanetName:
                return planetName if planetName else ""
            else:
                return ownerName if ownerName else ""
        elif relation == rFriend:
            return ownerName if ownerName else ""
        else:
            if radar_strength > 0:
                return ownerName if ownerName else ""
            else:
                return ""

    def IsPlayerAccount(self):
        return True

    def IsImpersonating(self):
        return self.request.user.is_impersonate

    '''
    sub Impersonate(new_userid)
        if Session(sPrivilege) >= 100 then
            UserId = new_userid
            Session.Contents(sUser) = new_userid
            Session("ImpersonatingUser") = Session(sLogonUserID) <> new_userid
    
            InvalidatePlanetList()
    
            CurrentPlanet = 0
            CurrentGalaxyId = 0
            CurrentSectorId = 0
    
            Response.Redirect "/s03/overview.asp"
            Response.End
        end if
    end sub
    '''
    
    def log_notice(self, title, details, level):
        '''
        query = "INSERT INTO log_notices (username, title, details, url, level) VALUES(" +\
                dosql(self.oPlayerInfo["username"]) + ", " +\
                dosql(title[:127]) + "," +\
                dosql(details[:127]) + "," +\
                dosql(self.scripturl[:127]) + "," +\
                str(level) +\
                ")"
        oConnDoQuery(query)
        '''
        return

    '''
    function Min(a, b)
        if a < b then Min = a else Min = b
    end function
    '''
    
    # Call this function when the name of a planet has changed or has been colonized or abandonned
    def InvalidatePlanetList(self):
        self.request.session[sPlanetList] = None

    # return image of a planet according to its it and its floor
    def planetimg(self,id,floor):
        img = 1+(floor + id) % 21
        if img < 10: img = "0" + str(img)
        return str(img)

    # return the percentage of the current value compared to max value
    def getpercent(self, current, max, slice):
        if (current >= max) or (max == 0):
            return 100
        else:
            return slice*int(100 * current / max / slice)

    #
    # Parse the header, list the planets owned by the player and show the resources of the current planet
    #
    def FillHeader(self, tpl):
        if self.CurrentPlanet == 0:
            return

        # Initialize the header
        tpl_header = tpl

        # retrieve player credits and assign the value, don't use oPlayerInfo as the info may be outdated
        query = "SELECT credits, prestige_points FROM users WHERE id=" + str(self.UserId) + " LIMIT 1"
        oRs = oConnExecute(query)
        tpl_header.AssignValue("money", oRs[0])
        tpl_header.AssignValue("pp", oRs[1])
    
        # assign current planet ore, hydrocarbon, workers and energy
        query = "SELECT ore, ore_production, ore_capacity," + \
                "hydrocarbon, hydrocarbon_production, hydrocarbon_capacity," + \
                "workers, workers_busy, workers_capacity," + \
                "energy_consumption, energy_production," + \
                "floor_occupied, floor," + \
                "space_occupied, space, workers_for_maintenance," + \
                "mod_production_ore, mod_production_hydrocarbon, energy, energy_capacity, soldiers, soldiers_capacity, scientists, scientists_capacity" +\
                " FROM vw_planets WHERE id="+str(self.CurrentPlanet)
        oRs = oConnExecute(query)
    
        tpl_header.AssignValue("ore", oRs[0])
        tpl_header.AssignValue("ore_production", oRs[1])
        tpl_header.AssignValue("ore_capacity", oRs[2])
    
        # compute ore level : ore / capacity
        ore_level = self.getpercent(oRs[0], oRs[2], 10)
    
        if ore_level >= 90:
            tpl_header.Parse("high_ore")
        elif ore_level >= 70:
            tpl_header.Parse("medium_ore")
        else:
            tpl_header.Parse("normal_ore")
    
        tpl_header.AssignValue("hydrocarbon", oRs[3])
        tpl_header.AssignValue("hydrocarbon_production", oRs[4])
        tpl_header.AssignValue("hydrocarbon_capacity", oRs[5])
    
        hydrocarbon_level = self.getpercent(oRs[3], oRs[5], 10)
    
        if hydrocarbon_level >= 90:
            tpl_header.Parse("high_hydrocarbon")
        elif hydrocarbon_level >= 70:
            tpl_header.Parse("medium_hydrocarbon")
        else:
            tpl_header.Parse("normal_hydrocarbon")
    
        tpl_header.AssignValue("workers", oRs[6])
        tpl_header.AssignValue("workers_capacity", oRs[8])
        tpl_header.AssignValue("workers_idle", oRs[6] - oRs[7])
    
        if oRs[6] < oRs[15]: tpl_header.Parse("workers_low")
    
        tpl_header.AssignValue("soldiers", oRs[20])
        tpl_header.AssignValue("soldiers_capacity", oRs[21])
    
        if oRs[20]*250 < oRs[6]+oRs[22]: tpl_header.Parse("soldiers_low")
    
        tpl_header.AssignValue("scientists", oRs[22])
        tpl_header.AssignValue("scientists_capacity", oRs[23])
    
        tpl_header.AssignValue("energy_consumption", oRs[9])
        tpl_header.AssignValue("energy_totalproduction", oRs[10])
        tpl_header.AssignValue("energy_production", oRs[10]-oRs[9])
    
        tpl_header.AssignValue("energy", oRs[18])
        tpl_header.AssignValue("energy_capacity", oRs[19])
    
        if oRs[9] > oRs[10]: tpl_header.Parse("energy_low")
    
        if oRs[9] > oRs[10]: tpl_header.Parse("energy_production_minus")
        else: tpl_header.Parse("energy_production_normal")
    
        tpl_header.AssignValue("floor_occupied", oRs[11])
        tpl_header.AssignValue("floor", oRs[12])
    
        tpl_header.AssignValue("space_occupied", oRs[13])
        tpl_header.AssignValue("space", oRs[14])
    
        # ore/hydro production colors
        if oRs[16] >= 0 and oRs[6] >= oRs[15]:
            tpl_header.Parse("normal_ore_production")
        else:
            tpl_header.Parse("medium_ore_production")

        if oRs[17] >= 0 and oRs[6] >= oRs[15]:
            tpl_header.Parse("normal_hydrocarbon_production")
        else:
            tpl_header.Parse("medium_hydrocarbon_production")

        #
        # Fill the planet list
        #
        if self.url_extra_params != "":
            tpl_header.AssignValue("url", "?" + url_extra_params + "&planet=")
        else:
            tpl_header.AssignValue("url", "?planet=")

        # cache the list of planets as they are not supposed to change unless a colonization occurs
        # in case of colonization, let the colonize script reset the session value
        # retrieve planet list
        query = "SELECT id, name, galaxy, sector, planet" + \
                " FROM nav_planet" + \
                " WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.UserId) + \
                " ORDER BY id"
        oRs = oConnExecuteAll(query)

        if oRs == None:
            planetListCount = -1
        else:
            planetListArray = oRs
            planetListCount = len(oRs)

        self.request.session[sPlanetList] = planetListArray
        self.request.session[sPlanetListCount] = planetListCount

        planets = []
        for item in planetListArray:
            id = item[0]
    
            planet = {}
            planets.append(planet)
            
            planet["id"] = id
            planet["name"] = item[1]
            planet["g"] = item[2]
            planet["s"] = item[3]
            planet["p"] = item[4]
    
            if id == self.CurrentPlanet: planet["selected"] = True
    
        tpl_header.AssignValue("planets", planets)
    
        query = "SELECT buildingid" +\
                " FROM planet_buildings INNER JOIN db_buildings ON (db_buildings.id=buildingid AND db_buildings.is_planet_element)" +\
                " WHERE planetid="+str(self.CurrentPlanet)+\
                " ORDER BY upper(db_buildings.label)"
        oRs = oConnExecuteAll(query)
    
        i = 0
        if oRs:
            for item in oRs:

                if i % 3 == 0:
                    tpl_header.AssignValue("special1", getBuildingLabel(item[0]))
                elif i % 3 == 1:
                    tpl_header.AssignValue("special2", getBuildingLabel(item[0]))
                else:
                    tpl_header.AssignValue("special3", getBuildingLabel(item[0]))
                    tpl_header.Parse("special")
        
                i = i + 1
    
        if i % 3 != 0: tpl_header.Parse("special")

    def FillHeaderCredits(self, tpl_header):
        oRs = oConnExecute("SELECT credits FROM users WHERE id="+str(self.UserId))
        tpl_header.AssignValue("credits", oRs[0])
    
    #
    # Parse the menu
    #
    def FillMenu(self, tpl_layout):
        # Initialize the menu template

        tpl = tpl_layout
    
        # retrieve number of new messages & reports
        query = "SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=" + str(self.UserId) + " AND read_date is NULL)," + \
                "(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=" + str(self.UserId) + " AND read_date is NULL AND datetime <= now());"
        oRs = oConnExecute(query)
        
        if oRs[0] > 0:
            tpl.AssignValue("new_mail", oRs[0])

        if oRs[1] > 0:
            tpl.AssignValue("new_report", oRs[1])

        if self.oAllianceRights:
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_manage_description"] or self.oAllianceRights["can_manage_announce"]: tpl.Parse("show_management")
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_see_reports"]: tpl.Parse("show_reports")
            if self.oAllianceRights["leader"] or self.oAllianceRights["can_see_members_info"]: tpl.Parse("show_members")
    
        if self.SecurityLevel >= 3:
            tpl.Parse("show_mercenary")
            tpl.Parse("show_alliance")
    
        #
        # Fill admin info
        #
        if self.request.session.get("privilege", 0) >= 100:
            
            query = "SELECT int4(MAX(id)) FROM log_http_errors"
            oRs = oConnExecute(query)
            last_errorid = oRs[0]
    
            query = "SELECT int4(MAX(id)) FROM log_notices"
            oRs = oConnExecute(query)
            last_noticeid = oRs[0]
    
            query = "SELECT COALESCE(dev_lasterror, 0), COALESCE(dev_lastnotice, 0) FROM users WHERE id=" + self.request.session.get(sLogonUserID)
            oRs = oConnExecute(query)
            if last_errorid > oRs[0]:
                tpl.AssignValue("new_error", last_errorid-oRs[0])
    
            if last_noticeid > oRs[1]:
                tpl.AssignValue("new_notice", last_noticeid-oRs[1])
    
            tpl.Parse("dev")
    
        tpl.AssignValue("planetid", self.CurrentPlanet)
    
        tpl.AssignValue("cur_g", self.CurrentGalaxyId)
        tpl.AssignValue("cur_s", self.CurrentSectorId)
        tpl.AssignValue("cur_p", ((self.CurrentPlanet-1) % 25) + 1)
    
        tpl.AssignValue("selectedmenu", self.selected_menu.replace(".","_"))
    
        if self.selected_menu != "":
            blockname = self.selected_menu + "_selected"
    
            while blockname != "":
                tpl.Parse(blockname)
    
                i = blockname.rfind(".")
                if i > 0: i = i - 1
                blockname = blockname[:i]

        # Assign the menu
        tpl_layout.AssignValue("menu", True)

    def logpage(self):
        self.pagelogged = True

    '''
    sub RedirectTo(url)
        logpage()
    
        pageTerminated = true
    
        Response.Redirect url
        Response.End
    end sub
    '''
    
    '''
    sub displayXML(tpl)
        dim tpl_xml
        set tpl_xml = GetTemplate("layoutxml")
    
        dim oRs, query
    
        ' retrieve number of new messages & reports
        query = "SELECT (SELECT int4(COUNT(*)) FROM messages WHERE ownerid=" & UserId & " AND read_date is NULL)," & _
                "(SELECT int4(COUNT(*)) FROM reports WHERE ownerid=" & UserId & " AND read_date is NULL AND datetime <= now());"
        set oRs = oConn.Execute(query)
    
        tpl_xml.AssignValue "new_mail", oRs(0)
        tpl_xml.AssignValue "new_report", oRs(1)
    
        tpl_xml.AssignValue "content", tpl.output
        tpl_xml.AssignValue "selectedmenu", Replace(selected_menu,".","_")
        tpl_xml.Parse ""
    
        response.contentType = "text/xml"
    
        Session("details") = "sending page"
        response.write tpl_xml.output
    end sub
    '''

    #
    # Display the tpl content with the default layout template
    #
    def Display(self, tpl):
        
        if self.request.GET.get("xml") == "1":
            return self.displayXML(tpl)
        else:
            tpl_layout = tpl
    
            # Initialize the layout
            if self.oPlayerInfo["skin"]:
                tpl_layout.AssignValue("skin", self.oPlayerInfo["skin"])
            else:
                tpl_layout.AssignValue("skin", "s_transparent")

            tpl_layout.AssignValue("credits", self.oPlayerInfo["credits"])
            tpl_layout.AssignValue("prestige_points", self.oPlayerInfo["prestige_points"])

            #
            # Fill and parse the header template
            #
            if self.showHeader == True: self.FillHeader(tpl_layout)
    
            #
            # Fill and parse the menu template
            #
            self.FillMenu(tpl_layout)
    
            #
            # Fill and parse the layout template
            #
            if self.oPlayerInfo["timers_enabled"]: tpl_layout.AssignValue("timers_enabled", "true")
            else: tpl_layout.AssignValue("timers_enabled", "false")
    
            #Assign the context/header
            if self.showHeader == True:
                tpl_layout.Parse("context")

            # Assign the scroll value if is assigned
            tpl_layout.AssignValue("scrolly", self.scrollY)
            if self.scrollY != 0: tpl_layout.Parse("scroll")
            
            if self.oPlayerInfo["deletion_date"]:
                tpl_layout.AssignValue("delete_datetime", self.oPlayerInfo["deletion_date"])
                tpl_layout.Parse("deleting")

            if self.oPlayerInfo["credits"] < 0:
                bankrupt_hours = self.oPlayerInfo["credits_bankruptcy"]
    
                tpl_layout.AssignValue("bankruptcy_hours", bankrupt_hours)
                tpl_layout.Parse("hours")
    
                tpl_layout.Parse("creditswarning")

            if self.IsImpersonating():
                tpl_layout.AssignValue("username", self.oPlayerInfo["username"])
                tpl_layout.Parse("impersonating")
                
            #
            # Fill admin info
            #
            '''
            if self.request.session.get(sPrivilege) > 100:
    
                # Assign the time taken to generate the page
                tpl_layout.AssignValue("render_time",  (time.clock() - self.StartTime))
    
                # Assign number of logged players
                oRs = oConnExecute("SELECT int4(count(*)) FROM vw_players WHERE lastactivity >= now()-INTERVAL '20 minutes'")
                tpl_layout.AssignValue("players", oRs[0])
                tpl_layout.Parse("dev")
    
                if self.oPlayerInfo["privilege"] == -2:
                    oRs = oConnExecute("SELECT start_time, min_end_time, end_time FROM users_holidays WHERE userid="+str(self.UserId))
    
                    if oRs:
                        tpl_layout.AssignValue("start_datetime", oRs[0])
                        tpl_layout.AssignValue("min_end_datetime", oRs[1])
                        tpl_layout.AssignValue("end_datetime", oRs[2])
                        tpl_layout.Parse("onholidays")
    
                if self.oPlayerInfo["privilege"] == -1:
                    tpl_layout.AssignValue("ban_datetime", self.oPlayerInfo["ban_datetime"])
                    tpl_layout.AssignValue("ban_reason", self.oPlayerInfo["ban_reason"])
                    tpl_layout.AssignValue("ban_reason_public", self.oPlayerInfo["ban_reason_public"])
    
                    if self.oPlayerInfo["ban_expire"]:
                        tpl_layout.AssignValue("ban_expire_datetime", self.oPlayerInfo["ban_expire"])
                        tpl_layout.Parse("banned.expire")
    
                    tpl_layout.Parse("banned")
            '''
            
            tpl_layout.AssignValue("userid", self.UserId)
            tpl_layout.AssignValue("server", universe)
    
            '''
            if not oPlayerInfo("paid") and Session(sPrivilege) < 100:
    
                connectNexusDB
                set oRs = oNexusConn.Execute("SELECT sp_ad_get_code(" & UserId & ")")
                if not oRs.EOF:
                    if not isnull(oRs[0]):
                        tpl_layout.AssignValue("ad_code", oRs[0]
                        tpl_layout.Parse("ads.code"
                    end if
                end if
    
                tpl_layout.Parse("ads"
                oConn.Execute "UPDATE users SET displays_pages=displays_pages+1 WHERE id=" & UserId
            '''
            
            tpl_layout.Parse("menu")
    
            if not self.oPlayerInfo["inframe"]:
                tpl_layout.Parse("test_frame")
            
            #
            # Write the template to the client
            #
            self.request.session["details"] = "sending page"
    
        self.logpage()

        return render(self.request, tpl_layout.template, tpl_layout.data)

    #
    # Check that our user is valid, otherwise redirect user to home page
    #
    def CheckSessionValidity(self):
        self.UserId = self.request.session.get(sUser)
    
        # check that this session is still used
        # if a user tries to login multiple times, the first sessions are abandonned

        query = "SELECT username, privilege, lastlogin, credits, lastplanetid, deletion_date, score, planets, previous_score," +\
                "alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance," +\
                "credits_bankruptcy, mod_planets, mod_commanders," +\
                "ban_datetime, ban_expire, ban_reason, ban_reason_public, orientation, (paid_until IS NOT NULL AND paid_until > now()) AS paid," +\
                " timers_enabled, display_alliance_planet_name, prestige_points, (inframe IS NOT NULL AND inframe) AS inframe, COALESCE(skin, 's_default') AS skin," +\
                "lcid, security_level" +\
                " FROM users" +\
                " WHERE id=" + str(self.UserId)
        self.oPlayerInfo = oConnRow(query)
        
        # check account still exists or that the player didn't connect with another account meanwhile
        if self.oPlayerInfo == None:
            return HttpResponseRedirect("/") # Redirect to home page
    
        self.SecurityLevel = self.oPlayerInfo["security_level"]
        self.displayAlliancePlanetName = self.oPlayerInfo["display_alliance_planet_name"]
    
        self.request.session["LCID"] = self.oPlayerInfo["lcid"]
        
        '''
        if self.request.session.get(sPrivilege) < 100:
            if self.request.COOKIES.get("username") == "":
                self.request.COOKIES["username"] = self.oPlayerInfo["username"]
            elif self.request.COOKIES.get("username") != self.oPlayerInfo["username"]:
                self.log_notice("username cookie", "Last browser username cookie : \"" + self.request.COOKIES.get("username", "") + "\"", 1)
                
                self.request.COOKIES["username"] = self.oPlayerInfo["username"]
        '''
        
        if self.oPlayerInfo["privilege"] == -1: return HttpResponseRedirect("/s03/locked/")
        if self.oPlayerInfo["privilege"] == -2: return HttpResponseRedirect("/s03/holidays/")
        if self.oPlayerInfo["privilege"] == -3: return HttpResponseRedirect("/s03/wait/")
        
        if self.oPlayerInfo["credits_bankruptcy"] <= 0: return HttpResponseRedirect("/s03/game-over/")

        self.AllianceId = self.oPlayerInfo["alliance_id"]
        self.AllianceRank = self.oPlayerInfo["alliance_rank"]
        self.oAllianceRights = None
    
        if self.AllianceId:
            query = "SELECT label, leader, can_invite_player, can_kick_player, can_create_nap, can_break_nap, can_ask_money, can_see_reports, can_accept_money_requests, can_change_tax_rate, can_mail_alliance," +\
                    " can_manage_description, can_manage_announce, can_see_members_info, can_use_alliance_radars, can_order_other_fleets" +\
                    " FROM alliances_ranks" +\
                    " WHERE allianceid=" + str(self.AllianceId) + " AND rankid=" + str(self.AllianceRank)
            self.oAllianceRights = oConnRow(query)
    
            if self.oAllianceRights == None:
                self.oAllianceRights = None
                self.AllianceId = None

        # log activity
        if not self.IsImpersonating(): oConnExecute("SELECT sp_log_activity(" + str(self.UserId) + "," + dosql(self.request.META.get("REMOTE_ADDR")) + ", 0)")

    # set the new current planet, if the planet doesn't belong to the player then go back to the session planet
    def SetCurrentPlanet(self, planetid):
    
        #
        # Check if a parameter is given and if different than the current planet
        # In that case, try to set it as the new planet : check that this planet belongs to the player
        #
        if (planetid != "") and (planetid != self.CurrentPlanet):
            # check that the new planet belongs to the player
            oRs = oConnExecute("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(planetid) + " and ownerid=" + str(self.UserId))
            if oRs:
                self.CurrentPlanet = planetid
                self.CurrentGalaxyId = oRs[0]
                self.CurrentSectorId = oRs[1]
                self.request.session[sPlanet] = planetid
    
                # save the last planetid
                if not self.request.user.is_impersonate:
                    oConnDoQuery("UPDATE users SET lastplanetid=" + str(planetid) + " WHERE id=" + str(self.UserId))
    
                return
    
            self.InvalidatePlanetList()
    
        # 
        # retrieve current planet from session
        #
        self.CurrentPlanet = self.request.session.get(sPlanet, "")
    
        if self.CurrentPlanet != None:
            # check if the planet still belongs to the player
            oRs = oConnExecute("SELECT galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND id=" + str(self.CurrentPlanet) + " AND ownerid=" + str(self.UserId))
            if oRs:
                # the planet still belongs to the player, exit
                self.CurrentGalaxyId = oRs[0]
                self.CurrentSectorId = oRs[1]
                return
    
            self.InvalidatePlanetList()
    
        # there is no active planet, select the first planet available
        oRs = oConnExecute("SELECT id, galaxy, sector FROM nav_planet WHERE planet_floor > 0 AND planet_space > 0 AND ownerid=" + str(self.UserId) + " LIMIT 1")
    
        # if player owns no planets then the game is over
        if oRs == None:
            return HttpResponseRedirect("/s03/game-over/")
    
        # assign planet id
        self.CurrentPlanet = oRs[0]
        self.CurrentGalaxyId = oRs[1]
        self.CurrentSectorId = oRs[2]
        self.request.session[sPlanet] = self.CurrentPlanet
    
        # save the last planetid
        if not self.request.user.is_impersonate:
            oConnDoQuery("UPDATE users SET lastplanetid=" + str(self.CurrentPlanet) + " WHERE id=" + str(self.UserId))
    
        # a player may wish to destroy a building on a planet that belonged to him
        # if the planet doesn't belong to him anymore, the action may be performed on another planet
        # so we redirect the user to the overview to prevent executing an order on another planet
        return HttpResponseRedirect("/s03/overview/")
    
    #
    # check if a planet is given in the querystring and that it belongs to the player
    #
    def CheckCurrentPlanetValidity(self):
    
        # retrieve planet parameter if any
        id = ToInt(self.request.GET.get("planet"), "")
    
        return self.SetCurrentPlanet(id)
