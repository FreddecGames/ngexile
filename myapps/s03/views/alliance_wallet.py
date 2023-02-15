# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "alliance.wallet"

        self.e_no_error = 0
        self.e_not_enough_money = 1
        self.e_can_give_money_after_a_week = 2

        self.money_error = self.e_no_error

        if self.AllianceId == None:
            return HttpResponseRedirect("/s03/overview/")

        #
        # accept/deny money self.request
        #
        action = self.request.GET.get("a", "")
        id = ToInt(self.request.GET.get("id"), 0)

        if action == "accept":
            oConnExecute("SELECT sp_alliance_money_accept(" + str(self.UserId) + "," + str(id) + ")")
        elif action == "deny":
            oConnExecute("SELECT sp_alliance_money_deny(" + str(self.UserId) + "," + str(id) + ")")

        #
        # player gives or self.requests credits
        #
        credits = ToInt(request.POST.get("credits"), 0)
        description = self.request.POST.get("description", "").strip()

        if self.request.POST.get("cancel", "") != "":
            credits = 0
            description = ""
            oConnExecute("SELECT sp_alliance_money_request("+str(self.UserId)+","+str(credits)+","+dosql(description)+")")

        if credits != 0:
            if self.request.POST.get("request", "") != "":
                oConnExecute("SELECT sp_alliance_money_request("+str(self.UserId)+","+str(credits)+","+dosql(description)+")")
            elif self.request.POST.get("give") != "" and (credits > 0):

                if self.can_give_money():
                    oRs = oConnExecute("SELECT sp_alliance_transfer_money("+str(self.UserId)+","+str(credits)+","+dosql(description)+",0)")
                    if oRs[0] != 0: self.money_error = self.e_not_enough_money
                else:
                    self.money_error = self.e_can_give_money_after_a_week

        #
        # change of tax rates
        #
        taxrates = request.POST.get("taxrates", "")

        if taxrates != "":
            connExecuteRetryNoRecords("SELECT sp_alliance_set_tax("+str(self.UserId)+","+dosql(taxrates)+")")

        #
        # retrieve which page is displayed
        #
        category = ToInt(request.GET.get("cat"), 1)

        if not self.oAllianceRights["can_ask_money"] and category == 2: category = 1
        if not self.oAllianceRights["can_change_tax_rate"] and category == 4: category = 1

        if category == 2:
            return self.DisplayRequests(2)
        elif category == 3:
            return self.DisplayGifts(3)
        elif category == 4:
            return self.DisplayTaxRates(4)
        elif category == 5:
            return self.DisplayHistoric(5)
        else:
            return self.DisplayJournal(1)

    def can_give_money(self):

        oRs = oConnExecute("SELECT game_started < now() - INTERVAL '2 weeks' FROM users WHERE id=" + str(self.UserId))

        return oRs and oRs[0]

    #
    # display the wallet page
    #
    def DisplayPage(self, tpl, cat):

        tpl.setValue("walletpage", cat)

        oRs = oConnExecute("SELECT credits, tax FROM alliances WHERE id=" + str(self.AllianceId))
        tpl.setValue("credits", oRs[0])
        tpl.setValue("tax", oRs[1]/10)

        if self.oPlayerInfo["planets"] < 2: tpl.Parse("notax")

        oRs = oConnExecute("SELECT COALESCE(sum(credits), 0) FROM alliances_wallet_journal WHERE allianceid=" + str(self.AllianceId) + " AND datetime >= now()-INTERVAL '24 hours'")
        tpl.setValue("last24h", oRs[0])

        if self.money_error == self.e_not_enough_money:
            tpl.Parse("not_enough_money")
        elif self.money_error == self.e_can_give_money_after_a_week:
            tpl.Parse("can_give_money_after_a_week")

        tpl.Parse("cat"+str(cat)+"_selected")

        tpl.Parse("cat1")
        if self.oAllianceRights["can_ask_money"]: tpl.Parse("cat2")
        tpl.Parse("cat3")
        if self.oAllianceRights["can_change_tax_rate"]: tpl.Parse("cat4")

        return self.display(tpl)

    #
    # display a journal of the last money operations
    # This is viewable by everybody
    #
    def DisplayJournal(self, cat):
        content = getTemplate(self.request, "s03/alliance-wallet-journal")
        content.setValue("walletpage", cat)

        col = ToInt(self.request.GET.get("col"), 0)
        if col < 1 or col > 4: col = 1

        reversed = False
        if col == 1:
            orderby = "datetime"
            reversed = True
        elif col == 2:
            orderby = "type"
            reversed = True
        elif col == 3:
            orderby = "upper(source)"
            reversed = True
        elif col == 4:
            orderby = "upper(destination)"
            reversed = True
        elif col == 5:
            orderby = "credits"
        elif col == 6:
            orderby = "upper(description)"

        if self.request.GET.get("r", "") != "":
            reversed = not reversed
        else:
            content.Parse("r" + str(col))

        if reversed: orderby = orderby + " DESC"
        orderby = orderby + ", datetime DESC"

        if self.request.POST.get("refresh", "") != "":
            displayGiftsRequests = ToInt(self.request.POST.get("gifts"), 0) == 1
            displaySetTax = ToInt(self.request.POST.get("settax"), 0) == 1
            displayTaxes = ToInt(self.request.POST.get("taxes"), 0) == 1
            displayKicksBreaks = ToInt(self.request.POST.get("kicksbreaks"), 0) == 1

            query = "UPDATE users SET" + \
                    " wallet_display[1]=" + str(displayGiftsRequests) + \
                    " ,wallet_display[2]=" + str(displaySetTax) + \
                    " ,wallet_display[3]=" + str(displayTaxes) + \
                    " ,wallet_display[4]=" + str(displayKicksBreaks) + \
                    " WHERE id=" + str(self.UserId)
            oConnDoQuery(query)
        else:
            query = "SELECT COALESCE(wallet_display[1], True)," + \
                    " COALESCE(wallet_display[2], True)," + \
                    " COALESCE(wallet_display[3], True)," + \
                    " COALESCE(wallet_display[4], True)" + \
                    " FROM users" + \
                    " WHERE id=" + str(self.UserId)
            oRs = oConnExecute(query)

            displayGiftsRequests = oRs[0]
            displaySetTax = oRs[1]
            displayTaxes = oRs[2]
            displayKicksBreaks = oRs[3]

        if displayGiftsRequests: content.Parse("gifts_checked")
        if displaySetTax: content.Parse("settax_checked")
        if displayTaxes: content.Parse("taxes_checked")
        if displayKicksBreaks: content.Parse("kicksbreaks_checked")

        query = ""
        if not displayGiftsRequests: query = query + " AND type != 0 AND type != 3 AND type != 20"
        if not displaySetTax: query = query + " AND type != 4"
        if not displayTaxes: query = query + " AND type != 1"
        if not displayKicksBreaks: query = query + " AND type != 2 AND type != 5 AND type != 10 AND type != 11"

        # List wallet journal
        query = "SELECT Max(datetime), userid, int4(sum(credits)), description, source, destination, type, groupid"+ \
                " FROM alliances_wallet_journal"+ \
                " WHERE allianceid=" + str(self.AllianceId) + query + " AND datetime >= now()-INTERVAL '1 week'"+ \
                " GROUP BY userid, description, source, destination, type, groupid"+ \
                " ORDER BY Max(datetime) DESC"+ \
                " LIMIT 500"

        oRss = oConnExecuteAll(query)

        if oRss == None: content.Parse("noentries")

        i = 1
        list = []
        content.setValue("entries", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["date"] = oRs[0]

            if oRs[2] > 0:
                item["income"] = oRs[2]
                item["outcome"] = 0
            else:
                item["income"] = 0
                item["outcome"] = -oRs[2]

            item["description"] = oRs[3] if oRs[3] else ""
            item["source"] = oRs[4] if oRs[4] else ""
            item["destination"] = oRs[5] if oRs[5] else ""

            if oRs[6] == 0: # gift
                item["gift"] = True
            elif oRs[6] == 1: # tax
                item["tax"] = True
            elif oRs[6] == 2:
                item["member_left"] = True
            elif oRs[6] == 3:
                item["money_request"] = True
            elif oRs[6] == 4:
                item["description"] = str(int(oRs[3])/10) + " %"
                item["taxchanged"] = True
            elif oRs[6] == 5:
                item["member_kicked"] = True
            elif oRs[6] == 10:
                item["nap_broken"] = True
            elif oRs[6] == 11:
                item["nap_broken"] = True
            elif oRs[6] == 12:
                item["war_cost"] = True
            elif oRs[6] == 20:
                item["tribute"] = True

        return self.DisplayPage(content, cat)

    #
    # display the self.requests page
    # Allow a player to self.request money from his alliance
    # Treasurer and Leader can see the list of self.request and accept/deny them
    #
    def DisplayRequests(self, cat):
        content = getTemplate(self.request, "s03/alliance-wallet-requests")
        content.setValue("walletpage", cat)

        oRs = oConnExecute("SELECT credits FROM users WHERE id=" + str(self.UserId))
        credits = oRs[0]

        content.setValue("player_credits", credits)

        query = "SELECT credits, description, result" + \
                " FROM alliances_wallet_requests" + \
                " WHERE allianceid=" + str(self.AllianceId) + " AND userid=" + str(self.UserId)

        oRs = oConnExecute(query)

        if oRs == None:
            content.Parse("request_none")
        else:
            content.setValue("req_credits", oRs[0])
            content.setValue("req_description", oRs[1])
            if (oRs[2]) and not oRs[2]: content.Parse("request_denied")
            else: content.Parse("request_submitted")

        content.Parse("request")

        if self.oAllianceRights["can_accept_money_requests"]:
            # List money self.requests
            query = "SELECT r.id, datetime, username, r.credits, r.description" + \
                    " FROM alliances_wallet_requests r" + \
                    "    INNER JOIN users ON users.id=r.userid" + \
                    " WHERE allianceid=" + str(self.AllianceId) + " AND result IS NULL"

            oRss = oConnExecuteAll(query)
            
            content.Parse("list")
            
            i = 0
            list = []
            content.setValue("entries", list)
            for oRs in oRss:
                item = {}
                list.append(item)
            
                item["id"] = oRs[0]
                item["date"] = oRs[1]
                item["nation"] = oRs[2]
                item["credits"] = oRs[3]
                item["description"] = oRs[4]

                i = i + 1

            if i == 0: content.Parse("norequests")

        return self.DisplayPage(content, cat)

    #
    #
    #
    def DisplayGifts(self, cat):
        content = getTemplate(self.request, "s03/alliance-wallet-give")
        content.setValue("walletpage", cat)

        oRs = oConnExecute("SELECT credits FROM users WHERE id=" + str(self.UserId))
        content.setValue("player_credits", oRs[0])

        if self.can_give_money():
            content.Parse("can_give")
        else:
            content.Parse("can_give_after_a_week")

        content.Parse("give")

        if self.oAllianceRights["can_accept_money_requests"]:
            # list gifts for the last 7 days

            query = "SELECT datetime, credits, source, description" + \
                    " FROM alliances_wallet_journal" + \
                    " WHERE allianceid="+str(self.AllianceId)+" AND type=0 AND datetime >= now()-INTERVAL '1 week'" + \
                    " ORDER BY datetime DESC"
            oRss = oConnExecuteAll(query)
            
            content.Parse("list")
            
            if oRss == None: content.Parse("noentries")

            list = []
            content.setValue("entries", list)
            for oRs in oRss:
                item = {}
                list.append(item)
                
                item["date"] = oRs[0]
                item["credits"] = oRs[1]
                item["nation"] = oRs[2]
                item["description"] = oRs[3]

        return self.DisplayPage(content, cat)

    #
    # display the tax rates page, only viewable by treasurer and leader
    #
    def DisplayTaxRates(self, cat):

        content = getTemplate(self.request, "s03/alliance-wallet-taxrates")
        content.setValue("walletpage", cat)

        oRs = oConnExecute("SELECT tax FROM alliances WHERE id=" + str(self.AllianceId))
        tax = oRs[0]

        # List available taxes
        list = []
        content.setValue("taxes", list)
        for i in range(0, 20):
            item = {}
            list.append(item)
            item["tax"] =  i*0.5
            item["taxrates"] = i*5

            if i*5 == tax: item["selected"] = True

        return self.DisplayPage(content, cat)

    def log10(self, n):
        return log(n) / log(100000)

    #
    # display credits income/outcome historic
    #
    def DisplayHistoric(self, cat):
        content = getTemplate(self.request, "s03/alliance-wallet-historic")
        content.setValue("walletpage", cat)

        query = "SELECT date_trunc('day', datetime), int4(sum(GREATEST(0, credits))), int4(-sum(LEAST(0, credits)))" + \
                " FROM alliances_wallet_journal" + \
                " WHERE allianceid=" + str(self.AllianceId) + \
                " GROUP BY date_trunc('day', datetime)" + \
                " ORDER BY date_trunc('day', datetime)"
        oRss = oConnExecuteAll(query)

        maxValue = 0
        for oRs in oRss:
            if oRs[1] > maxValue: maxValue = oRs[1]
            if oRs[2] > maxValue: maxValue = oRs[2]

        list = []
        content.setValue("entries", list)
        for oRs in oRss:
            item = {}
            list.append(item)

            item["income_height"] = int(400 * oRs[1] / maxValue)
            item["outcome_height"] = int(400 * oRs[2] / maxValue)
            item["income"] = oRs[1]
            item["outcome"] = oRs[2]
            item["datetime"] = oRs[0]
            item["day"] = True

        return self.DisplayPage(content, cat)
