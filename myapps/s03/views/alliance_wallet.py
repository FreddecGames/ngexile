from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post
        
        action = self.request.POST.get('action', '')
        if action == 'set_tax':
            
            taxrate = ToInt(request.POST.get('taxrate'), 0)            
            oConnDoQuery('SELECT sp_alliance_set_tax(' + str(self.UserId) + ',' + str(taxrate) + ')')
        
        #--- get
        
        self.selectedMenu = 'alliance'

        content = GetTemplate(self.request, 'alliance-wallet')

        dbRow = oConnRow('SELECT credits, tax FROM alliances WHERE id=' + str(self.AllianceId))
        content.AssignValue('alliance_credits', dbRow['credits'])
        content.AssignValue('alliance_tax', dbRow['tax'] / 10)
        
        if self.oPlayerInfo['planets'] < 2: content.Parse('notax')

        dbRow = oConnRow('SELECT COALESCE(sum(credits), 0) AS credits FROM alliances_wallet_journal WHERE allianceid=' + str(self.AllianceId) + ' AND datetime >= now() - INTERVAL \'24 hours\'')
        content.AssignValue('last24h', dbRow['credits'])

        taxes = []
        content.AssignValue('taxes', taxes)
        
        for i in range(0, 20):
        
            item = {}
            taxes.append(item)
            
            item['tax'] = i * 0.5
            item['taxrate'] = i * 5

        query = 'SELECT Max(datetime) AS date, userid, int4(sum(credits)) AS credits, description, source, destination, type, groupid' + \
                ' FROM alliances_wallet_journal' + \
                ' WHERE allianceid=' + str(self.AllianceId) + ' AND datetime >= now() - INTERVAL \'1 week\' AND credits != 0' + \
                ' GROUP BY userid, description, source, destination, type, groupid' + \
                ' ORDER BY Max(datetime) DESC' + \
                ' LIMIT 50'
        dbRows = oConnRows(query)
        content.AssignValue('entries', dbRows)

        return self.Display(content)
