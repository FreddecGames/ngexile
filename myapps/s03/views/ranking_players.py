# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "ranking.players"

        return self.DisplayRanking()

    def DisplayRanking(self):
        content = GetTemplate(self.request, "s03/ranking-players")

        #
        # Setup search by Alliance and Nation query string
        #
        searchbyA = ""
        searchbyN = ""

        searchby = searchbyA + searchbyN

        # if the page is a search result, add the search params to column ordering links
        if searchby != "": content.Parse("search_params")

        #
        # Setup column ordering
        #
        col = ToInt(self.request.GET.get("col"), 3)
        if col < 1 or col > 4: col = 3

        reversed = False
        if col == 1:
            orderby = "CASE WHEN score_visibility=2 OR v.id="+str(self.UserId)+"THEN upper(login) ELSE '' END, upper(login)"
        elif col == 2:
            orderby = "upper(alliances.name)"
        elif col == 3:
            orderby = "v.score"
            reversed = True
        elif col == 4:
            orderby = "v.score_prestige"
            reversed = True

        if self.request.GET.get("r", "") != "":
            reversed = not reversed
        else:
            content.Parse("r" + str(col))

        if reversed: orderby = orderby + " DESC"
        orderby = orderby + ", upper(login)"

        content.AssignValue("sort_column", col)

        #
        # get the score of the tenth user to only show the avatars of the first 10 players
        #
        query = "SELECT score" + \
                " FROM vw_players" + \
                " WHERE True "+searchby + \
                " ORDER BY score DESC OFFSET 9 LIMIT 1"
        oRs = oConnExecute(query)

        if oRs == None:
            TenthUserScore = 0
        else:
            TenthUserScore = oRs[0]

        displayed = 100 # number of nations displayed per page

        #
        # Retrieve the offset from where to begin the display
        #
        offset = ToInt(self.request.GET.get("start"), -1)

        if offset < 0:
            query = "SELECT v.id" + \
                    " FROM vw_players v LEFT JOIN alliances ON alliances.id=v.alliance_id" + \
                    " WHERE True "+searchby + \
                    " ORDER BY "+orderby
            oRss = oConnExecuteAll(query)

            index = 0
            found = False
            for oRs in oRss:
                if oRs[0] == self.UserId:
                    found = True
                    break

                index = index +1

            myOffset = int(index/displayed)
            if not found: myOffset=0
            offset = myOffset

        # get total number of players that could be displayed
        query = "SELECT count(1) FROM vw_players WHERE True "+searchby
        oRs = oConnExecute(query)
        size = int(oRs[0])
        nb_pages = int(size/displayed)
        if nb_pages*displayed < size: nb_pages = nb_pages + 1
        if offset >= nb_pages: offset = nb_pages-1
        if offset < 0: offset = 0

        content.AssignValue("page_displayed", offset+1)
        content.AssignValue("page_first", offset*displayed+1)
        content.AssignValue("page_last", min(size, (offset+1)*displayed))

        idx_from = offset+1 - 10
        if idx_from < 1: idx_from = 1

        idx_to = offset+1 + 10
        if idx_to > nb_pages: idx_to = nb_pages

        list = []
        content.AssignValue("ps", list)
        for i in range(1, nb_pages+1):
            if (i==1) or (i >= idx_from and i <= idx_to) or (i % 10 == 0):
                item = {}
                list.append(item)
                
                item["page_id"] = i
                item["page_link"] = i-1
    
                if i-1 != offset:
                    if searchby != "": item["search_params"] = True
                    if self.request.GET.get("r", "") != "": item["reversed"] = True
    
                    item["link"] = True
                else:
                    item["selected"] = True

        #display only if there are more than 1 page
        if nb_pages > 1: content.Parse("nav")

        # Retrieve players to display
        query = "SELECT login, v.score, v.score_prestige," + \
                "COALESCE(date_part('day', now()-lastactivity), 15), alliances.name, alliances.tag, v.id, avatar_url, v.alliance_id, v.score-v.previous_score AS score_delta," + \
                "v.score >= " + str(TenthUserScore) + " OR score_visibility = 2 OR (score_visibility = 1 AND alliance_id IS NOT NULL AND alliance_id="+str(sqlValue(self.AllianceId))+") OR v.id="+str(self.UserId) + \
                " FROM vw_players v" + \
                "    LEFT JOIN alliances ON ((v.score >= " + str(TenthUserScore) + " OR score_visibility = 2 OR v.id="+str(self.UserId)+" OR (score_visibility = 1 AND alliance_id IS NOT NULL AND alliance_id="+str(sqlValue(self.AllianceId))+")) AND alliances.id=v.alliance_id)" + \
                " WHERE True "+searchby + \
                " ORDER BY "+orderby+" OFFSET "+str(offset*displayed)+" LIMIT "+str(displayed)
        oRss = oConnExecuteAll(query)

        if oRs == None: content.Parse("noresult")

        i = 1
        list = []
        content.AssignValue("players", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["place"] = offset*displayed+i
            item["username"] = oRs[0]

            visible = oRs[10]

            if visible and oRs[4]:
                item["alliancename"] = oRs[4]
                item["alliancetag"] = oRs[5]
                item["alliance"] = True
            else:
                item["noalliance"] = True

            item["score"] = oRs[1]
            item["score_battle"] = oRs[2]
            if visible:
                item["score_delta"] = oRs[9]
                if oRs[9] > 0: item["plus"] = True
                if oRs[9] < 0: item["minus"] = True
            else:
                item["score_delta"] = ""

            item["stat_colonies"] = oRs[2]
            item["last_login"] = oRs[3]

            if oRs[3] <= 7:
                item["recently"] = True
            elif oRs[3] <= 14:
                item["1weekplus"] = True
            elif oRs[3] > 14:
                item["2weeksplus"] = True

            if visible:
                if oRs[6] == self.UserId:
                    item["self"] = True
                elif self.AllianceId and oRs[8] == self.AllianceId:
                    item["ally"] = True

                # show avatar only if top 10
                if oRs[1] >= TenthUserScore:
                    if oRs[7] == None or oRs[7] == "":
                        item["noavatar"] = True
                    else:
                        item["avatar_url"] = oRs[7]
                        item["avatar"] = True

                    item["top10avatar"] = True

                item["name"] = True
            else:
                item["name_na"] = True

            i = i + 1

        return self.Display(content)
