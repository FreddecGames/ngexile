# -*- coding: utf-8 -*-

from myapps.api.views._permissions import *

#---

class View(BaseView):
    permission_classes = [ IsAuthenticated, IsActive ]

    ################################################################################
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.data['action']
        
        #---
        
        if action == 'sendmail' and not request.user.is_impersonate:
            
            mailto = request.POST.get('to', '').strip()
            if request.POST.get('type') == 'alliance': mailto = ':alliance'
            if mailto == '':
                messages.error(request, 'mail_missing_to')
                return HttpResponseRedirect('/s03/mail-new/')
                
            mailbody = request.POST.get('message', '').strip()
            if mailbody == '':
                messages.error(request, 'mail_empty')
                return HttpResponseRedirect('/s03/mail-new/')
                
            mailsubject = request.POST.get('subject', '').strip()

            if ToInt(request.POST.get('sendcredits'), 0) == 1: moneyamount = ToInt(request.POST.get('amount'), 0)
            else: moneyamount = 0            
            if request.POST.get('type') == 'alliance': moneyamount = 0

            bbcode = request.POST.get('self.bbcode') == 1

            result = dbExecute('SELECT sp_send_message(' + str(self.userId) + ',' + dosql(mailto) + ',' + dosql(mailsubject) + ',' + dosql(mailbody) + ',' + str(moneyamount) + ',' + str(bbcode) + ')')
            if result == 0: messages.success(request, 'mail_sent')
            elif result == 1: messages.error(request, 'mail_unknown_from')
            elif result == 2: messages.error(request, 'mail_unknown_to')
            elif result == 3: messages.error(request, 'mail_same')
            elif result == 4: messages.error(request, 'not_enough_credits')
            elif result == 9: messages.error(request, 'blocked')       
        
        #---
            
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
        
        #---
        
        tpl = getTemplate()
            
        #---
        
        mailto = ''
        mailbody = ''
        mailsubject = ''
        
        if request.GET.get('to', '') != '':
        
            mailto = request.GET.get('to', '')
            mailsubject = request.GET.get('subject', '')
            
        elif request.GET.get('a', '') == 'new':

            mailto = request.GET.get('b', '')
            if mailto == '': mailto = request.GET.get('to', '')
            
            mailsubject = request.GET.get('subject', '')

        elif request.GET.get('a', '') == 'reply':

            mailId = ToInt(request.GET.get('mailid'), 0)

            query = 'SELECT sender, subject, body FROM messages WHERE ownerid=' + str(self.userId) + ' AND id=' + str(mailId) + ' LIMIT 1'
            mail = dbRow(query)
            if mail:

                mailto = mail['sender']

                if 'Re:' in mail['subject']: mailsubject = mail['subject']
                else: mailsubject = 'Re: ' + mail['subject']
                
                body = '> ' + mail['body'] + '\n'
                body.replace('\n', '\n' + '> ') + '\n\n'
                mailbody = body
        
        tpl.set('mailto', mailto)
        tpl.set('subject', mailsubject)
        tpl.set('message', mailbody)

        #---
        
        query = 'SELECT username' + \
                ' FROM messages_addressee_history INNER JOIN users ON messages_addressee_history.addresseeid = users.id' + \
                ' WHERE ownerid=' + str(self.userId) + \
                ' ORDER BY upper(username)'
        results = dbRows(query)
        
        tpl.set('addressees', results)

        #---
        
        if self.allianceRights and self.allianceRights['can_mail_alliance']: tpl.set('can_sendalliance')
        
        #---
        
        player = dbRow('SELECT credits, (now() - game_started > INTERVAL \'2 weeks\') AS can_sendcredit FROM users WHERE id=' + str(self.userId))
        tpl.set('player', player)
        
        #---

        return Response(tpl.data)
