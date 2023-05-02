# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        #---
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        
        #---
        
        self.selectedMenu = "ranking"

        content = getTemplate(request, "s03/ranking-alliances")

        #---

        col = ToInt(request.GET.get("col"), 2)
        if col < 1 or col > 7: col = 1

        if col == 5: col = 1
        
        if col == 1:
            orderby = "upper(alliances.name)"
            reversed = False
        elif col == 2:
            orderby = "score"
            reversed = True
        elif col == 3:
            orderby = "members"
            reversed = True
        elif col == 4:
            orderby = "planets"
            reversed = True
        elif col == 6:
            orderby = "created"
            reversed = False
        elif col == 7:
            orderby = "upper(alliances.tag)"
            reversed = False

        content.setValue('col', col)
        
        #---
        
        if request.GET.get('r', '') != '': reversed = not reversed
        else: content.Parse('r' + str(col))
        
        #---
        
        if reversed: orderby = orderby + " DESC"
        orderby = orderby + ", upper(alliances.name)"
        
        #---

        offset = ToInt(request.GET.get("start"), -1)
        if offset < 0: offset = 0

        displayed = 25

        query = "SELECT count(DISTINCT alliance_id) FROM users INNER JOIN alliances ON alliances.id=alliance_id WHERE alliances.visible"
        size = dbExecute(query)

        nb_pages = int(size / displayed)
        if nb_pages * displayed < size: nb_pages = nb_pages + 1
        if offset >= nb_pages: offset = nb_pages - 1
        if offset < 0: offset = 0

        if nb_pages > 1:
        
            content.setValue("page_displayed", offset+1)
            content.setValue("page_first", offset*displayed+1)
            content.setValue("page_last", min(size, (offset+1)*displayed))

            idx_from = offset + 1 - 10
            if idx_from < 1: idx_from = 1

            idx_to = offset + 1 + 10
            if idx_to > nb_pages: idx_to = nb_pages

            pages = []
            content.setValue("pages", pages)
            
            for i in range(1, nb_pages + 1):
                if i == 1 or (i >= idx_from and i <= idx_to) or i % 10 == 0:
                
                    item = {}
                    pages.append(item)
                    
                    item["id"] = i
                    item["link"] = i - 1
        
                    if i - 1 == offset: item["selected"] = True
                    elif request.GET.get("r") != "": item["reversed"] = True
        
        #---

        query = "SELECT alliances.id, alliances.tag, alliances.name, sum(users.score) AS score, count(*) AS members, sum(planets) AS planets," + \
                " int4(alliances.score / count(*)) AS score_average, sum(users.score)-sum(users.previous_score) as score_delta," + \
                " created, EXISTS(SELECT 1 FROM alliances_naps WHERE allianceid1=alliances.id AND allianceid2=" + str(sqlValue(self.allianceId)) + ") AS nap," + \
                " max_members, EXISTS(SELECT 1 FROM alliances_wars WHERE (allianceid1=alliances.id AND allianceid2=" + str(sqlValue(self.allianceId)) + ") OR (allianceid1=" + str(sqlValue(self.allianceId)) + " AND allianceid2=alliances.id)) AS war" + \
                " FROM users INNER JOIN alliances ON alliances.id=alliance_id" + \
                " WHERE alliances.visible" + \
                " GROUP BY alliances.id, alliances.name, alliances.tag, alliances.score, alliances.previous_score, alliances.created, alliances.max_members" + \
                " ORDER BY " + orderby + \
                " OFFSET " + str(offset * displayed) + " LIMIT " + str(displayed)
        rows = dbRows(query)

        content.setValue("alliances", rows)
        
        i = 1
        for row in rows:
        
            row["place"] = offset * displayed + i

            if self.allianceId and row['id'] == self.allianceId: row["playeralliance"] = True

            i = i + 1
        
        #---
        
        return self.display(content, request)
