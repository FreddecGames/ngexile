from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- get
        
        self.selectedMenu = 'ranking'

        content = getTemplateContext(self.request, 'ranking-players')

        query = 'SELECT users.id, username, users.score, avatar_url,' + \
                ' alliance_id, alliances.name, alliances.tag, avatar_url, (users.score - users.previous_score) AS score_delta,' + \
                ' (score_visibility = 2 OR (score_visibility = 1 AND alliance_id IS NOT NULL AND alliance_id=' + str(sqlValue(self.AllianceId)) + ') OR users.id=' + str(self.profile['id']) + ') AS score_visibility' + \
                ' FROM vw_players AS users' + \
                '    LEFT JOIN alliances ON ((score_visibility = 2 OR users.id=' + str(self.profile['id']) + ' OR (score_visibility = 1 AND alliance_id IS NOT NULL AND alliance_id=' + str(sqlValue(self.AllianceId)) + ')) AND alliances.id = alliance_id)' + \
                ' ORDER BY users.score DESC'
        dbRows = dbRows(query)

        list = []
        content.assignValue('players', list)
        
        i = 1
        for dbRow in dbRows:
        
            item = {}
            list.append(item)
            
            item['place'] = i
            
            item['score'] = dbRow['score']
            
            if dbRow['score_visibility']:
            
                item['username'] = dbRow['username']
                item['avatar_url'] = dbRow['avatar_url']
                item['score_delta'] = dbRow['score_delta']
                
                if dbRow['tag']:
                    item['alliance_tag'] = dbRow['tag']
                    item['alliance_name'] = dbRow['name']
                    
                if dbRow['id'] == self.profile['id']: item['self'] = True
                elif self.AllianceId and dbRow['alliance_id'] == self.AllianceId: item['ally'] = True

            i = i + 1

        return self.display(content)
