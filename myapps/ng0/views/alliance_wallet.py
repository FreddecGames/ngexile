from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        action = self.request.POST.get('action', '')
        
        if action == 'set_tax':
            
            taxrate = toInt(request.POST.get('taxrate'), 0)            
            dbQuery('SELECT sp_alliance_set_tax(' + str(self.profile['id']) + ',' + str(taxrate) + ')')
            
            return HttpResponseRedirect('/s03/alliance-wallet/')
            
        elif action == 'give':
            
            dbRow = dbRow('SELECT (game_started < now() - INTERVAL \'2 weeks\') AS result FROM users WHERE id=' + str(self.profile['id']))
            if dbRow and dbRow['result']:
                
                credits = toInt(request.POST.get('credits'), 0) 
                dbRow = dbRow('SELECT sp_alliance_transfer_money(' + str(self.profile['id']) + ',' + str(credits) + ', \'\', 0) AS result')
                if dbRow['result'] != 0: messages.error(request, 'give_error_' + str(dbRow['result']))
            
            else: messages.error(request, 'give_error_1')
            
            return HttpResponseRedirect('/s03/alliance-wallet/')
        
        #--- get
        
        self.selectedMenu = 'alliance'

        content = getTemplateContext(self.request, 'alliance-wallet')

        dbRow = dbRow('SELECT credits, tax FROM alliances WHERE id=' + str(self.AllianceId))
        content.assignValue('alliance_credits', dbRow['credits'])
        content.assignValue('alliance_tax', dbRow['tax'] / 10)
        
        if self.oPlayerInfo['planets'] < 2: content.parse('notax')

        dbRow = dbRow('SELECT COALESCE(sum(credits), 0) AS credits FROM alliances_wallet_journal WHERE allianceid=' + str(self.AllianceId) + ' AND datetime >= now() - INTERVAL \'24 hours\'')
        content.assignValue('last24h', dbRow['credits'])

        taxes = []
        content.assignValue('taxes', taxes)
        
        for i in range(0, 20):
        
            item = {}
            taxes.append(item)
            
            item['tax'] = i * 0.5
            item['taxrate'] = i * 5
        
        dbRow = dbRow('SELECT (game_started < now() - INTERVAL \'2 weeks\') AS result FROM users WHERE id=' + str(self.profile['id']))
        if dbRow and dbRow['result']: content.parse('can_give')
        
        query = 'SELECT Max(datetime) AS date, userid, int4(sum(credits)) AS credits, description, source, destination, type, groupid' + \
                ' FROM alliances_wallet_journal' + \
                ' WHERE allianceid=' + str(self.AllianceId) + ' AND datetime >= now() - INTERVAL \'1 week\' AND credits != 0' + \
                ' GROUP BY userid, description, source, destination, type, groupid' + \
                ' ORDER BY Max(datetime) DESC' + \
                ' LIMIT 50'
        dbRows = dbRows(query)
        content.assignValue('entries', dbRows)

        return self.display(content)
