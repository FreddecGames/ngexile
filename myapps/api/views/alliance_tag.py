# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---        

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tag = request.GET.get('tag', '')
        
        #---

        tpl = getTemplate()
        
        #---
        
        query = 'SELECT id, name, tag, description, (SELECT count(*) FROM users WHERE alliance_id=alliances.id) AS members,' + \
                ' logo_url, max_members' + \
                ' FROM alliances'
        if tag == '': query = query + ' WHERE id=' + str(self.allianceId) + ' LIMIT 1'            
        else: query = query + ' WHERE tag=upper(' + dosql(tag) + ') LIMIT 1'
        
        alliance = dbRow(query)
        tpl.set('alliance', alliance)
        
        #---
        
        query = 'SELECT rankid, label' + \
                ' FROM alliances_ranks' + \
                ' WHERE members_displayed AND allianceid=' + str(alliance['id']) + \
                ' ORDER BY rankid'
                
        ranks = dbRows(query)
        tpl.set('ranks', ranks)
        
        #---
        
        for rank in ranks:
        
            query = 'SELECT username' + \
                    ' FROM users' + \
                    ' WHERE alliance_id=' + str(alliance['id']) + ' AND alliance_rank = ' + str(rank['rankid']) + \
                    ' ORDER BY upper(username)'
                    
            members = dbRows(query)
            rank['members'] = members
        
        #---
        
        query = 'SELECT tag, name' + \
                ' FROM alliances_naps INNER JOIN alliances ON (alliances_naps.allianceid1=alliances.id)' + \
                ' WHERE allianceid2=' + str(alliance['id'])
                
        naps = dbRows(query)
        tpl.set('naps', naps)
        
        #---

        query = 'SELECT alliances.tag, alliances.name'+ \
                ' FROM alliances_wars w' + \
                '    INNER JOIN alliances ON (allianceid2 = alliances.id)' + \
                ' WHERE allianceid1=' + str(alliance['id']) + \
                ' UNION ' + \
                'SELECT alliances.tag, alliances.name'+ \
                ' FROM alliances_wars w' + \
                '    INNER JOIN alliances ON (allianceid1 = alliances.id)' + \
                ' WHERE allianceid2=' + str(alliance['id'])
            
        wars = dbRows(query)
        tpl.set('wars', wars)
        
        #---
        
        return Response(tpl.data)
