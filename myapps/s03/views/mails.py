# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        #---

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #---
        
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        
        #---
        
        if request.POST.get("sendmail", "") != "" and not request.user.is_impersonate:
            
            mailto = request.POST.get("to", "").strip()
            if request.POST.get("type") == "alliance": mailto = ":alliance"
            if mailto == "":
                messages.error(request, 'mail_missing_to')
                return HttpResponseRedirect('/s03/mails/?a=new')
                
            mailbody = request.POST.get("message", "").strip()
            if mailbody == "":
                messages.error(request, 'mail_empty')
                return HttpResponseRedirect('/s03/mails/?a=new')
                
            mailsubject = request.POST.get("subject", "").strip()

            if ToInt(request.POST.get("sendcredits"), 0) == 1: moneyamount = ToInt(request.POST.get("amount"), 0)
            else: moneyamount = 0
            if request.POST.get("type") == "alliance": moneyamount = 0

            bbcode = request.POST.get("self.bbcode") == 1

            result = dbExecute("SELECT sp_send_message(" + str(self.userId) + "," + dosql(mailto) + "," + dosql(mailsubject) + "," + dosql(mailbody) + "," + str(moneyamount) + "," + str(bbcode) + ")")
            if result == 0: messages.success(request, 'mail_sent')
            elif result == 1: messages.error(request, 'mail_unknown_from')
            elif result == 2: messages.error(request, 'mail_unknown_to')
            elif result == 3: messages.error(request, 'mail_same')
            elif result == 4: messages.error(request, 'not_enough_credits')
            elif result == 9: messages.error(request, 'blocked')
            
            return HttpResponseRedirect('/s03/mails/?a=new')       
        
        #---
        
        elif request.POST.get("action", "") == "delete":
            
            mailId = ToInt(request.POST.get("mailId"), 0)            
            if mailId != 0:
                dbQuery("UPDATE messages SET deleted=TRUE WHERE id=" + str(mailId) + " AND ownerid = " + str(self.userId))
            
            return HttpResponseRedirect('/s03/mails/')
            
        #---
            
        return HttpResponseRedirect('/s03/mails/')
        
    def get(self, request, *args, **kwargs):
            
        #---

        if request.GET.get("a", "") == "ignore":
        
            dbExecute("SELECT sp_ignore_sender(" + str(self.userId) + "," + dosql(request.GET.get("user")) + ")")
            return HttpResponseRedirect('/s03/mails/')
            
        #---

        elif request.GET.get("a", "") == "unignore":
        
            dbQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.userId) + " AND ignored_userid=(SELECT id FROM users WHERE lower(username)=lower(" + dosql(request.GET.get("user")) + "))")
            return HttpResponseRedirect('/s03/mails/')
            
        #---
        
        elif request.GET.get("a") == "ignorelist" or request.GET.get("a") == "unignorelist":
            
            #---
            
            self.selectedMenu = "mails"

            content = getTemplate(request, "s03/mail-ignorelist")

            #---
            ignorednations = dbRows("SELECT ignored_userid AS userid, sp_get_user(ignored_userid) AS name, added, blocked FROM messages_ignore_list WHERE userid=" + str(self.userId))
            content.setValue("ignorednations", ignorednations)

            return self.display(content, request)
            
        #---
        
        elif request.GET.get("a") == "sent":
        
            #---
            
            self.selectedMenu = "mails"
            
            content = getTemplate(request, "s03/mail-sent")
            
            #---
            
            displayed = 30

            query = "SELECT count(1) FROM messages WHERE datetime > now()-INTERVAL '2 weeks' AND senderid = " + str(self.userId)
            size = int(dbExecute(query))
            nb_pages = int(size / displayed)
            if nb_pages * displayed < size: nb_pages = nb_pages + 1
            if nb_pages > 50: nb_pages = 50
            
            #---
            
            offset = ToInt(request.GET.get("start"), 0)
            if offset > 50: offset = 50
            if offset < 0: offset = 0
            if offset >= nb_pages: offset = nb_pages - 1
            if offset < 0: offset = 0
            
            content.setValue("offset", offset)

            #---
            
            pages = []
            content.setValue("pages", pages)
            for i in range(1, nb_pages + 1):
            
                item = {}
                pages.append(item)
                
                item["id"] = i
                item["link"] = i - 1

                if i == offset + 1: item["selected"] = True

            content.setValue("min", offset * displayed + 1)
            if offset + 1 == nb_pages: content.setValue("max", size)
            else: content.setValue("max", (offset + 1) * displayed)

            content.setValue("page_display", offset + 1)
            
            #---
            
            query = "SELECT messages.id, owner, avatar_url, datetime, subject, body, messages.credits, users.id, bbcode, alliances.tag" + \
                    " FROM messages" + \
                    "    LEFT JOIN users ON (users.id = messages.ownerid AND messages.datetime >= users.game_started)" + \
                    "    LEFT JOIN alliances ON (users.alliance_id = alliances.id)" + \
                    " WHERE datetime > now()-INTERVAL '2 weeks' AND senderid = " + str(self.userId) + \
                    " ORDER BY datetime DESC OFFSET " + str(offset * displayed) + " LIMIT " + str(displayed)
            mails = dbRows(query)
            content.setValue("mails", mails)
            
            for mail in mails:
                mail['body'] = mail['body'].replace('\n', '<br/>')
            
            #---
            
            return self.display(content, request)
            
        #---
        
        mailto = None
        mailbody = None
        mailsubject = None
        
        if request.GET.get("to", "") != "":
        
            mailto = request.GET.get("to", "")
            mailsubject = request.GET.get("subject", "")
            
        elif request.GET.get("a", "") == "new":

            mailto = request.GET.get("b", "")
            if mailto == "": mailto = request.GET.get("to", "")
            
            mailsubject = request.GET.get("subject", "")

        elif request.GET.get("a", "") == "reply":

            mailId = ToInt(request.GET.get("mailid"), 0)

            query = "SELECT sender, subject, body FROM messages WHERE ownerid=" + str(self.userId) + " AND id=" + str(mailId) + " LIMIT 1"
            mail = dbRow(query)
            if mail:

                mailto = mail['sender']

                if "Re:" in mail['subject']: mailsubject = mail['subject']
                else: mailsubject = "Re: " + mail['subject']
                
                body = "> " + mail['body'] + "\n"
                body.replace("\n", "\n" + "> ") + "\n\n"
                mailbody = body
        
        if mailto != None or mailsubject != None or mailbody != None:
            
            #---
            
            self.selectedMenu = "mails"
            
            content = getTemplate(request, "s03/mail-compose")

            #---
            
            content.setValue("mailto", mailto)
            content.setValue("subject", mailsubject)
            content.setValue("message", mailbody)

            #---
            
            query = 'SELECT username' + \
                    ' FROM messages_addressee_history INNER JOIN users ON messages_addressee_history.addresseeid = users.id' + \
                    ' WHERE ownerid=' + str(self.userId) + \
                    ' ORDER BY upper(username)'
            results = dbRows(query)
            
            content.setValue("addressees", results)

            #---
            
            if self.allianceRights and self.allianceRights["can_mail_alliance"]: content.Parse("can_sendalliance")
            
            #---
            
            player = dbRow("SELECT credits, (now() - game_started > INTERVAL '2 weeks' AND security_level >= 3) AS can_sendcredit FROM users WHERE id=" + str(self.userId))
            content.setValue("player", player)
            
            #---

            return self.display(content, request)
            
        #---
        
        else:
            
            #---
            
            self.selectedMenu = "mails"
            
            content = getTemplate(request, "s03/mail-list")
            
            #---
            
            displayed = 30

            query = "SELECT count(1) FROM messages WHERE deleted=False AND ownerid = " + str(self.userId)
            size = int(dbExecute(query))
            nb_pages = int(size / displayed)
            if nb_pages * displayed < size: nb_pages = nb_pages + 1
            if nb_pages > 50: nb_pages = 50
            
            #---
            
            offset = ToInt(request.GET.get("start"), 0)
            if offset > 50: offset = 50
            if offset < 0: offset = 0
            if offset >= nb_pages: offset = nb_pages - 1
            if offset < 0: offset = 0
            
            content.setValue("offset", offset)

            #---
            
            pages = []
            content.setValue("pages", pages)
            for i in range(1, nb_pages + 1):
            
                item = {}
                pages.append(item)
                
                item["id"] = i
                item["link"] = i - 1

                if i == offset + 1: item["selected"] = True

            content.setValue("min", offset * displayed + 1)
            if offset + 1 == nb_pages: content.setValue("max", size)
            else: content.setValue("max", (offset + 1) * displayed)

            content.setValue("page_display", offset + 1)

            #---

            query = "SELECT sender, subject, body, datetime, messages.id AS mailid, read_date, avatar_url, users.id AS userid, messages.credits," + \
                    " users.privilege, bbcode, owner, messages_ignore_list.added, alliances.tag" + \
                    " FROM messages" + \
                    "    LEFT JOIN users ON (upper(users.username) = upper(messages.sender) AND messages.datetime >= users.game_started)" + \
                    "    LEFT JOIN alliances ON (users.alliance_id = alliances.id)" + \
                    "    LEFT JOIN messages_ignore_list ON (userid=" + str(self.userId) + " AND ignored_userid = users.id)" + \
                    " WHERE deleted=False AND ownerid = " + str(self.userId) + \
                    " ORDER BY datetime DESC, messages.id DESC" + \
                    " OFFSET " + str(offset * displayed) + " LIMIT " + str(displayed)
            mails = dbRows(query)
            content.setValue("mails", mails)
            
            for mail in mails:
                mail['body'] = mail['body'].replace('\n', '<br/>')
                
            #---
            
            if not request.user.is_impersonate:
                dbQuery("UPDATE messages SET read_date = now() WHERE ownerid = " + str(self.userId) + " AND read_date IS NULL" )

            #---
            
            return self.display(content, request)
