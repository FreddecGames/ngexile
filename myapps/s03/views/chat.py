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
        
        action = request.GET.get('a')
        
        #---
        
        if action == 'send':
        
            chatid = ToInt(request.GET.get('id'), 0)
            
            msg = request.GET.get('l', '').strip()[:260]
            
            if msg != '':
                dbQuery('INSERT INTO chat_lines(chatid, allianceid, userid, username, message) VALUES(' + str(chatid) + ',' + str(sqlValue(self.allianceId)) + ',' + str(self.userId) + ',' + dosql(self.profile['username']) + ',' + dosql(msg) + ')')
            
            return HttpResponse('')
        
        #---

        elif action == 'refresh':
            
            userchatid = -1
            chatid = ToInt(request.GET.get('id'), 0)
            if chatid == 0 and self.allianceId:
                userchatid = 0
                chatid = dbExecute('SELECT chatid FROM alliances WHERE id=' + str(self.allianceId))
            
            lastmsgid = request.session.get('lastchatmsg_' + str(chatid), '')
            if lastmsgid == '': lastmsgid = 0
            
            tpl = getTemplate(request, 'chat-handler')
            
            query = 'SELECT chat_lines.id, datetime, allianceid, username, message, alliances.tag' + \
                    ' FROM chat_lines' + \
                    '  LEFT JOIN alliances ON (chat_lines.allianceid=alliances.id)' + \
                    ' WHERE chat_lines.chatid=' + str(chatid) + ' AND chat_lines.id > GREATEST((SELECT id FROM chat_lines WHERE chatid=' + str(chatid) +' ORDER BY datetime DESC OFFSET 100 LIMIT 1), ' + str(lastmsgid) + ')' + \
                    ' ORDER BY chat_lines.id'
            lines = dbRows(query)
            tpl.set('lines', lines)
            
            if len(lines) > 0:
                request.session['lastchatmsg_' + str(chatid)] = lines[len(lines) - 1]['id']
            
            query = 'SELECT users.alliance_id, users.username, date_part(\'epoch\', now()-chat_onlineusers.lastactivity) AS lastactivity, alliances.tag' + \
                    ' FROM chat_onlineusers' + \
                    '  INNER JOIN users ON (users.id=chat_onlineusers.userid)' + \
                    '  LEFT JOIN alliances ON (users.alliance_id=alliances.id)' + \
                    ' WHERE chat_onlineusers.lastactivity > now()-INTERVAL \'10 minutes\' AND chat_onlineusers.chatid=' + str(chatid)
            users = dbRows(query)
            tpl.set('users', users)
            
            tpl.set('refresh', True)
            
            if userchatid == 0: tpl.set('chatid', 0)
            else: tpl.set('chatid', chatid)
            
            return render(request, tpl.template, tpl.data)
        
        #---
            
        elif action == 'join':
            
            tpl = getTemplate(request, 'chat-handler')
            
            pwd = request.GET.get('pass', '').strip()
            chatname = request.GET.get('chat', '').strip()
            query = 'SELECT sp_chat_join(' + dosql(chatname) + ',' + dosql(pwd) + ')'
            result = dbExecute(query)
            
            if result != 0:
                
                chatid = result
                
                query = 'INSERT INTO users_chats(userid, chatid, password) VALUES(' + str(self.userId) + ',' + str(chatid) + ',' + dosql(pwd) + ')'
                dbQuery(query)
                
                query = 'SELECT id, name, topic FROM chat WHERE id=' + str(chatid)
                chat = dbRow(query)
                tpl.set('chat', chat)
                
                request.session['lastchatmsg_' + str(chatid)] = ''
                
                tpl.set('join')
                
            else:
                tpl.set('join_badpassword')
            
            return render(request, tpl.template, tpl.data)
            
        #---
            
        elif action == 'leave':
        
            chatid = ToInt(request.GET.get('id'), 0)
            
            request.session['lastchatmsg_' + str(chatid)] = ''            
            
            query = 'DELETE FROM users_chats WHERE userid=' + str(self.userId) + ' AND chatid=' + str(chatid)
            dbQuery(query)

            query = 'DELETE FROM chat WHERE id > 0 AND NOT public AND name IS NOT NULL AND id=' + str(chatid) + ' AND (SELECT count(1) FROM users_chats WHERE chatid=chat.id) = 0'
            dbQuery(query)
            
            return HttpResponse('')
            
        #---
        
        tpl = getTemplate(request, 'chat')

        self.selectedMenu = 'chat'
        
        #---
        
        tpl.set('username', self.profile['username'])
        tpl.set('now', timezone.now())
        
        #---

        if (self.allianceId):
            chatid = dbExecute('SELECT chatid FROM alliances WHERE id=' + str(self.allianceId))            
            dbQuery('INSERT INTO chat_onlineusers(chatid, userid) VALUES(' + str(chatid) + ',' + str(self.userId) + ')')
            request.session['lastchatmsg_' + str(chatid)] = ''
            tpl.set('alliance')

        #---
        
        query = 'SELECT chat.id, chat.name, chat.topic' + \
                ' FROM users_chats' + \
                '    INNER JOIN chat ON (chat.id=users_chats.chatid AND ((chat.password = \'\') OR (chat.password = users_chats.password)))' + \
                ' WHERE userid = ' + str(self.userId) + \
                ' ORDER BY users_chats.added'
        joins = dbRows(query)
        tpl.set('joins', joins)
        
        for join in joins:
            
            dbQuery('INSERT INTO chat_onlineusers(chatid, userid) VALUES(' + str(join['id']) + ',' + str(self.userId) + ')')
            
            request.session['lastchatmsg_' + str(join['id'])] = ''

        #---
        
        query = 'SELECT name, topic, count(chat_onlineusers.userid) AS online' + \
                ' FROM chat' + \
                '    LEFT JOIN chat_onlineusers ON (chat_onlineusers.chatid = chat.id AND chat_onlineusers.lastactivity > now()-INTERVAL \'10 minutes\')' + \
                ' WHERE name IS NOT NULL AND password = \'\' AND public' + \
                ' GROUP BY name, topic' + \
                ' ORDER BY length(name), name'
        chats = dbRows(query)
        
        tpl.set('chats', chats)

        #---

        return self.display(tpl, request)
