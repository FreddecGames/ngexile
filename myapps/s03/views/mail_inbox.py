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
    
    def post(self, request, *args, **kwargs):
        
        #---
        
        action = request.POST.get('action')
        
        #---
        
        if action == "delete":
            
            mailId = ToInt(request.POST.get("mailId"), 0)            
            if mailId != 0:
                dbQuery("UPDATE messages SET deleted=TRUE WHERE id=" + str(mailId) + " AND ownerid = " + str(self.userId))
            
        #---

        elif action == "ignore":
        
            dbQuery("SELECT sp_ignore_sender(" + str(self.userId) + "," + dosql(request.POST.get("user")) + ")")
            
        #---

        elif action == "unignore":
        
            dbQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.userId) + " AND ignored_userid=(SELECT id FROM users WHERE lower(username)=lower(" + dosql(request.POST.get("user")) + "))")
            
        #---
            
        return HttpResponseRedirect(request.build_absolute_uri())
        
    ################################################################################
    
    def get(self, request, *args, **kwargs):
            
        #---
        
        content = getTemplate(request, "s03/mail-list")
        
        self.selectedMenu = "mails"
        
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
