# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        if not self.allianceId:
            return HttpResponseRedirect('/s03/alliance/')
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        action = request.POST.get('a', '')

        if action == 'give' and self.can_give_money():
            
            credits = ToInt(request.POST.get("credits"), 0)
            description = request.POST.get("description", "").strip()
            result = dbExecute("SELECT sp_alliance_transfer_money(" + str(self.userId) + "," + str(credits) + "," + dosql(description) + ",0)")
            if result != 0: messages.error(request, 'not_enough_money')

        elif action == 'request' and self.allianceRights["can_ask_money"]:
        
            credits = ToInt(request.POST.get("credits"), 0)
            description = request.POST.get("description", "").strip()
            dbQuery("SELECT sp_alliance_money_request(" + str(self.userId) + "," + str(credits) + "," + dosql(description) + ")")

        elif action == 'cancel':
            
            dbQuery("SELECT sp_alliance_money_request(" + str(self.userId) + ", 0, NULL)")

        elif action == 'settax' and self.allianceRights["can_change_tax_rate"]:
            
            taxrates = request.POST.get("taxrates", "")
            dbQuery("SELECT sp_alliance_set_tax(" + str(self.userId) + "," + dosql(taxrates) + ")")
            
        return HttpResponseRedirect('/s03/alliance-wallet/')
        
    def get(self, request, *args, **kwargs):
            
        action = request.GET.get("a", "")

        if action == "accept" and self.allianceRights["can_accept_money_requests"]:
        
            id = ToInt(request.GET.get("id"), 0)
            dbExecute("SELECT sp_alliance_money_accept(" + str(self.userId) + "," + str(id) + ")")
            
        elif action == "deny" and self.allianceRights["can_accept_money_requests"]:
        
            id = ToInt(request.GET.get("id"), 0)
            dbExecute("SELECT sp_alliance_money_deny(" + str(self.userId) + "," + str(id) + ")")
        
        #---
        
        tpl = getTemplate(self.request, "s03/alliance-wallet")

        self.selectedMenu = "alliance.wallet"
        
        #---
        
        if self.allianceRights['can_ask_money']: tpl.Parse('can_ask')
        if self.allianceRights['can_change_tax_rate']: tpl.Parse('can_settax')
        if self.allianceRights['can_accept_money_requests']: tpl.Parse('can_accept')
        
        if self.can_give_money(): tpl.Parse('can_give')
        
        #---
        
        alliance = dbRow("SELECT credits, tax FROM alliances WHERE id=" + str(self.allianceId))        
        alliance = alliance | dbRow("SELECT COALESCE(sum(credits), 0) AS last24h FROM alliances_wallet_journal WHERE allianceid=" + str(self.allianceId) + " AND datetime >= now()-INTERVAL '24 hours'")      
        alliance['taxrate'] = alliance['tax'] / 10
        tpl.setValue("alliance", alliance)

        #---

        if self.profile["planets"] < 2: tpl.Parse("notax")

        #---
        
        if self.request.GET.get("refresh", "") != "":
        
            displayGiftsRequests = ToInt(self.request.GET.get("gifts"), 0) == 1
            displaySetTax = ToInt(self.request.GET.get("settax"), 0) == 1
            displayTaxes = ToInt(self.request.GET.get("taxes"), 0) == 1
            displayKicksBreaks = ToInt(self.request.GET.get("kicksbreaks"), 0) == 1

            query = "UPDATE users SET" + \
                    " wallet_display[1]=" + str(displayGiftsRequests) + \
                    " ,wallet_display[2]=" + str(displaySetTax) + \
                    " ,wallet_display[3]=" + str(displayTaxes) + \
                    " ,wallet_display[4]=" + str(displayKicksBreaks) + \
                    " WHERE id=" + str(self.userId)
            dbQuery(query)

        #---
    
        query = "SELECT COALESCE(wallet_display[1], True) AS displayGiftsRequests," + \
                " COALESCE(wallet_display[2], True) AS displaySetTax," + \
                " COALESCE(wallet_display[3], True) AS displayTaxes," + \
                " COALESCE(wallet_display[4], True) AS displayKicksBreaks" + \
                " FROM users" + \
                " WHERE id=" + str(self.userId)
        filters = dbRow(query)
        tpl.setValue("filters", filters)
        
        #---

        query = ""
        if not filters['displaygiftsrequests']: query = query + " AND type != 0 AND type != 3 AND type != 20"
        if not filters['displaysettax']: query = query + " AND type != 4"
        if not filters['displaytaxes']: query = query + " AND type != 1"
        if not filters['displaykicksbreaks']: query = query + " AND type != 2 AND type != 5 AND type != 10 AND type != 11"

        query = "SELECT Max(datetime) AS date, userid, int4(sum(credits)) AS credits, description, source, destination, type, groupid" + \
                " FROM alliances_wallet_journal" + \
                " WHERE allianceid=" + str(self.allianceId) + query + " AND datetime >= now()-INTERVAL '1 week'" + \
                " GROUP BY userid, description, source, destination, type, groupid" + \
                " ORDER BY Max(datetime) DESC" + \
                " LIMIT 500"
        entries = dbRows(query)
        tpl.setValue("entries", entries)

        #---
        
        user = dbRow("SELECT credits FROM users WHERE id=" + str(self.userId))
        tpl.setValue("user", user)

        #---
        
        query = "SELECT credits, description, result" + \
                " FROM alliances_wallet_requests" + \
                " WHERE allianceid=" + str(self.allianceId) + " AND userid=" + str(self.userId)
        user_request = dbRow(query)
        tpl.setValue("user_request", user_request)

        #---
        
        if self.allianceRights['can_accept_money_requests']:
            
            query = "SELECT r.id, datetime, username, r.credits, r.description" + \
                    " FROM alliances_wallet_requests r" + \
                    "  INNER JOIN users ON users.id=r.userid" + \
                    " WHERE allianceid=" + str(self.allianceId) + " AND result IS NULL"
            requests = dbRow(query)
            tpl.setValue("requests", requests)

        #---
        
        if self.allianceRights['can_accept_money_requests']:
            
            query = "SELECT datetime, credits, source, description" + \
                    " FROM alliances_wallet_journal" + \
                    " WHERE allianceid=" + str(self.allianceId)+" AND type=0 AND datetime >= now()-INTERVAL '1 week'" + \
                    " ORDER BY datetime DESC"
            gifts = dbRow(query)
            tpl.setValue("gifts", gifts)

        #---
        
        taxes = []
        tpl.setValue("taxes", taxes)
        
        for i in range(0, 20):
        
            item = {}
            taxes.append(item)
            
            item["tax"] =  i * 0.5
            item["taxrates"] = i * 5
            
        return self.display(tpl)

    def can_give_money(self):

        result = dbExecute("SELECT game_started < now() - INTERVAL '2 weeks' FROM users WHERE id=" + str(self.userId))
        return result
