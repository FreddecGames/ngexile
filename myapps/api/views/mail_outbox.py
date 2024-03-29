# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################
    
    def get(self, request, *args, **kwargs):
            
        #---
        
        tpl = getTemplate()
        
        #---
        
        displayed = 30

        query = 'SELECT count(1) FROM messages WHERE datetime > now()-INTERVAL \'2 weeks\' AND senderid = ' + str(self.userId)
        size = int(dbExecute(query))
        nb_pages = int(size / displayed)
        if nb_pages * displayed < size: nb_pages = nb_pages + 1
        if nb_pages > 50: nb_pages = 50
        
        #---
        
        offset = ToInt(request.GET.get('start'), 0)
        if offset > 50: offset = 50
        if offset < 0: offset = 0
        if offset >= nb_pages: offset = nb_pages - 1
        if offset < 0: offset = 0
        
        tpl.set('offset', offset)

        #---
        
        pages = []
        tpl.set('pages', pages)
        for i in range(1, nb_pages + 1):
        
            item = {}
            pages.append(item)
            
            item['id'] = i
            item['link'] = i - 1

            if i == offset + 1: item['selected'] = True

        tpl.set('min', offset * displayed + 1)
        if offset + 1 == nb_pages: tpl.set('max', size)
        else: tpl.set('max', (offset + 1) * displayed)

        tpl.set('page_display', offset + 1)
        
        #---
        
        query = 'SELECT messages.id, owner, avatar_url, datetime, subject, body, messages.credits, users.id, bbcode, alliances.tag' + \
                ' FROM messages' + \
                '    LEFT JOIN users ON (users.id = messages.ownerid AND messages.datetime >= users.game_started)' + \
                '    LEFT JOIN alliances ON (users.alliance_id = alliances.id)' + \
                ' WHERE datetime > now()-INTERVAL \'2 weeks\' AND senderid = ' + str(self.userId) + \
                ' ORDER BY datetime DESC OFFSET ' + str(offset * displayed) + ' LIMIT ' + str(displayed)
        mails = dbRows(query)
        tpl.set('mails', mails)
        
        for mail in mails:
            mail['body'] = mail['body'].replace('\n', '<br/>')
        
        #---
        
        return Response(tpl.data)
            