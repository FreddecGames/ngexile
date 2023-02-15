# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "merchants"

        self.ExecuteOrder()

        return self.DisplayMarket()

    # display market for current player's planets
    def DisplayMarket(self):

        # get market template

        content = GetTemplate(self.request, "s03/market-sell")

        planet = ToInt(self.request.GET.get("planet", "").strip(), 0)
        if planet != 0:
            planet_query = " AND v.id=" + str(planet)
            content.AssignValue("get_planet", planet)
        else: planet_query = ""

        # retrieve ore, hydrocarbon, sales quantities on the planet

        query = "SELECT id, name, galaxy, sector, planet, ore, hydrocarbon, ore_capacity, hydrocarbon_capacity, planet_floor," + \
                " ore_production, hydrocarbon_production," + \
                " (sp_market_price((sp_get_resource_price(0, galaxy)).sell_ore, planet_stock_ore))," + \
                " (sp_market_price((sp_get_resource_price(0, galaxy)).sell_hydrocarbon, planet_stock_hydrocarbon))" + \
                " FROM vw_planets AS v" + \
                " WHERE floor > 0 AND v.ownerid="+str(self.UserId) + planet_query + \
                " ORDER BY v.id"
        oRss = oConnExecuteAll(query)

        total = 0
        count = 0
        i = 1
        list = []
        content.AssignValue("m_planets", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            p_img = 1+(oRs[9] + oRs[0]) % 21
            if p_img < 10: p_img = "0" + str(p_img)

            item["index"] = i

            item["planet_img"] = p_img

            item["planet_id"] = oRs[0]
            item["planet_name"] = oRs[1]
            item["g"] = oRs[2]
            item["s"] = oRs[3]
            item["p"] = oRs[4]

            item["planet_ore"] = oRs[5]
            item["planet_hydrocarbon"] = oRs[6]

            item["planet_ore_capacity"] = oRs[7]
            item["planet_hydrocarbon_capacity"] = oRs[8]

            item["planet_ore_production"] = oRs[10]
            item["planet_hydrocarbon_production"] = oRs[11]

            item["ore_price"] = oRs[12]
            item["hydrocarbon_price"] = oRs[13]

            item["ore_price2"] = str(oRs[12]).replace( ",", ".")
            item["hydrocarbon_price2"] = str(oRs[13]).replace(",", ".")

            # if ore/hydrocarbon quantity reach their capacity in less than 4 hours
            if oRs[5] > oRs[7]-4*oRs[10]: item["high_ore_capacity"] = True
            if oRs[6] > oRs[8]-4*oRs[11]: item["high_hydrocarbon_capacity"] = True

            item["ore_max"] = min(10000, int(oRs[5]/1000))
            item["hydrocarbon_max"] = min(10000, int(oRs[6]/1000))

            item["selling_price"] = 0

            count = count + 1

            if oRs[0] == self.CurrentPlanet: item["highlight"] = True

            i = i + 1

        if planet_query != "":
            self.showHeader = True
            self.selected_menu = "planet"

            content.Parse("planetid")
        else:
            content.AssignValue("total", total)
            content.Parse("totalprice")

        if count > 0: content.Parse("sell")

        return self.Display(content)

    # execute sell orders
    def ExecuteOrder(self):

        if self.request.GET.get("a") != "sell": return

        # for each planet owned, check what the player sells
        query = "SELECT id FROM nav_planet WHERE ownerid="+str(self.UserId)
        planetsArray = oConnExecuteAll(query)

        for i in planetsArray:
            planetid = i[0]

            # retrieve ore + hydrocarbon quantities
            ore = ToInt(self.request.POST.get("o" + str(planetid)), 0)
            hydrocarbon = ToInt(self.request.POST.get("h" + str(planetid)), 0)

            if ore > 0 or hydrocarbon > 0:
                query = "SELECT sp_market_sell(" + str(self.UserId) + "," + str(planetid) + "," + str(ore*1000) + "," + str(hydrocarbon*1000) + ")"
                oRs = oConnExecute(query)
