# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    ################################################################################
    
    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        #---
        
        return super().dispatch(request, *args, **kwargs)

    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---

        tpl = getTemplate(request, 'ranking-players')

        self.selectedMenu = 'ranking'

        #---
        
        col = ToInt(request.GET.get('col'), 3)
        if col < 1 or col > 4: col = 3

        if col == 1:
            orderby = 'CASE WHEN score_visibility=2 OR v.id=' + str(self.userId) + ' THEN upper(username) ELSE \'\' END, upper(username)'
            reversed = False
        elif col == 2:
            orderby = 'upper(alliances.name)'
            reversed = False
        elif col == 3:
            orderby = 'v.score'
            reversed = True
        elif col == 4:
            orderby = 'v.score_prestige'
            reversed = True

        tpl.set('col', col)
        
        #---

        if request.GET.get('r', '') != '': reversed = not reversed
        else: tpl.set('r' + str(col))
        
        #---

        if reversed: orderby = orderby + ' DESC'
        orderby = orderby + ', upper(username)'
        
        #---
        
        query = 'SELECT score FROM vw_players ORDER BY score DESC OFFSET 9 LIMIT 1'
        TenthUserScore = dbExecute(query)
        if TenthUserScore == None: TenthUserScore = 0
        
        tpl.set('TenthUserScore', TenthUserScore)
        
        #---
        
        offset = ToInt(request.GET.get('start'), -1)
        if offset < 0: offset = 0

        displayed = 100

        query = 'SELECT count(1) FROM vw_players'
        size = dbExecute(query)
        
        nb_pages = int(size / displayed)
        if nb_pages * displayed < size: nb_pages = nb_pages + 1
        if offset >= nb_pages: offset = nb_pages - 1
        if offset < 0: offset = 0

        if nb_pages > 1:
        
            tpl.set('page_displayed', offset + 1)
            tpl.set('page_first', offset * displayed + 1)
            tpl.set('page_last', min(size, (offset + 1) * displayed))

            idx_from = offset + 1 - 10
            if idx_from < 1: idx_from = 1

            idx_to = offset + 1 + 10
            if idx_to > nb_pages: idx_to = nb_pages

            pages = []
            tpl.set('pages', pages)
            
            for i in range(1, nb_pages + 1):
                if i == 1 or (i >= idx_from and i <= idx_to) or i % 10 == 0:
                
                    item = {}
                    pages.append(item)
                    
                    item['id'] = i
                    item['link'] = i - 1
        
                    if i - 1 == offset: item['selected'] = True
                    elif request.GET.get('r') != '': item['reversed'] = True
        
        #---
        
        query = 'SELECT username, v.score, v.score_prestige,' + \
                ' COALESCE(date_part(\'day\', now() - lastactivity), 15) AS lastactivity, alliances.name AS alliancename, alliances.tag AS alliancetag, v.id, avatar_url, v.alliance_id, v.score-v.previous_score AS score_delta,' + \
                ' (v.score >= ' + str(TenthUserScore) + ' OR score_visibility = 2 OR (score_visibility = 1 AND alliance_id IS NOT NULL AND alliance_id=' + str(sqlValue(self.allianceId)) + ') OR v.id=' + str(self.userId) + ') AS visible' + \
                ' FROM vw_players v' + \
                '    LEFT JOIN alliances ON ((v.score >= ' + str(TenthUserScore) + ' OR score_visibility = 2 OR v.id=' + str(self.userId) + ' OR (score_visibility = 1 AND alliance_id IS NOT NULL AND alliance_id=' + str(sqlValue(self.allianceId)) + ')) AND alliances.id=v.alliance_id)' + \
                ' ORDER BY ' +orderby+' OFFSET ' + str(offset*displayed) + ' LIMIT ' + str(displayed)
        rows = dbRows(query)

        tpl.set('players', rows)

        i = 1
        for row in rows:
            
            row['place'] = offset * displayed + i
            
            if row['id'] == self.userId: row['self'] = True
            elif self.allianceId and row['alliance_id'] == self.allianceId: row['ally'] = True
            
            i = i + 1
        
        #---

        return self.display(tpl, request)
