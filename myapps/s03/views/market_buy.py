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

        content = GetTemplate(self.request, "s03/market-buy")

        get_planet = self.request.GET.get("planet", "").strip()
        if get_planet != "": get_planet = " AND v.id=" + dosql(get_planet)

        self.request.session["details"] = "list planets"

        # retrieve ore, hydrocarbon, sales quantities on the planet

        query = "SELECT v.id, v.name, v.galaxy, v.sector, v.planet, v.ore, v.hydrocarbon, v.ore_capacity, v.hydrocarbon_capacity, v.planet_floor," + \
                " v.ore_production, v.hydrocarbon_production," + \
                " m.ore, m.hydrocarbon, m.ore_price, m.hydrocarbon_price," + \
                " int4(date_part('epoch', m.delivery_time-now()))," + \
                " sp_get_planet_blocus_strength(v.id) >= v.space," + \
                " workers, workers_for_maintenance," + \
                " (SELECT has_merchants FROM nav_galaxies WHERE id=v.galaxy) as has_merchants," + \
                " (sp_get_resource_price(" + str(self.UserId) + ", v.galaxy)).buy_ore::real AS p_ore," + \
                " (sp_get_resource_price(" + str(self.UserId) + ", v.galaxy)).buy_hydrocarbon AS p_hydrocarbon" + \
                " FROM vw_planets AS v" + \
                "    LEFT JOIN market_purchases AS m ON (m.planetid=v.id)" + \
                " WHERE floor > 0 AND v.ownerid="+str(self.UserId) + get_planet + \
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
            item["planet_name"] =  oRs[1]
            item["g"] = oRs[2]
            item["s"] = oRs[3]
            item["p"] = oRs[4]

            item["planet_ore"] = oRs[5]
            item["planet_hydrocarbon"] = oRs[6]

            item["planet_ore_capacity"] = oRs[7]
            item["planet_hydrocarbon_capacity"] = oRs[8]

            item["planet_ore_production"] = oRs[10]
            item["planet_hydrocarbon_production"] = oRs[11]

            # if ore/hydrocarbon quantity reach their capacity in less than 4 hours
            if oRs[5] > oRs[7]-4*oRs[10]: item["high_ore_capacity"] = True
            if oRs[6] > oRs[8]-4*oRs[11]: item["high_hydrocarbon_capacity"] = True

            item["ore_max"] = int((oRs[7]-oRs[5])/1000)
            item["hydrocarbon_max"] = int((oRs[8]-oRs[6])/1000)

            item["price_ore"] = str(oRs[21]).replace(",", ".")
            item["price_hydrocarbon"] = str(oRs[22]).replace(",", ".")

            if oRs[12] or oRs[13]:
                item["buying_ore"] = oRs[12]
                item["buying_hydrocarbon"] = oRs[13]

                subtotal = oRs[12]/1000*oRs[14] + oRs[13]/1000*oRs[15]
                total = total + subtotal

                item["buying_price"] = int(subtotal)

                item["buying"] = True
                item["can_buy"] = True
            else:
                item["ore"] = self.request.POST.get("o" + str(oRs[0]))
                item["hydrocarbon"] = self.request.POST.get("h" + str(oRs[0]))

                item["buying_price"] = 0

                if not oRs[20]:
                    item["cant_buy_merchants"] = True
                elif oRs[18] < oRs[19] / 2:
                    item["cant_buy_workers"] = True
                elif oRs[17]:
                    item["cant_buy_enemy"] = True
                else:
                    item["buy"] = True
                    item["can_buy"] = True

                    count = count + 1

            if oRs[0] == self.CurrentPlanet: item["highlight"] = True

            i = i + 1

        if get_planet != "":
            self.showHeader = True
            self.selected_menu = "planet"

            content.AssignValue("get_planet", self.request.GET.get("planet", ""))
        else:
            self.FillHeaderCredits(content)
            content.AssignValue("total", int(total))
            content.Parse("totalprice")

        if count > 0: content.Parse("buy")

        return self.Display(content)

    # execute buy orders
    def ExecuteOrder(self):

        if self.request.GET.get("a", "") != "buy": return

        self.request.session["details"] = "Execute orders"

        # for each planet owned, check what the player buys
        query = "SELECT id FROM nav_planet WHERE ownerid="+str(self.UserId)
        planetsArray = oConnExecuteAll(query)

        for i in planetsArray:
            planetid = i[0]

            # retrieve ore + hydrocarbon quantities
            ore = ToInt(self.request.POST.get("o" + str(planetid)), 0)
            hydrocarbon = ToInt(self.request.POST.get("h" + str(planetid)), 0)

            if ore > 0 or hydrocarbon > 0:

                query = "SELECT * FROM sp_buy_resources(" + str(self.UserId) + "," + str(planetid) + "," + str(ore*1000) + "," + str(hydrocarbon*1000) + ")"
                self.request.session["details"] = query
                oConnDoQuery(query)
                self.request.session["details"] = "done:"+query
