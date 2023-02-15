# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils.dateparse import parse_date

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.onlineusers_refreshtime = 60

        self.selectedMenu = "chat"

        chatid = ToInt(request.GET.get("id"), 0)
        action = request.GET.get("a")

        if action == "send":
            return self.addLine(chatid, request.GET.get("l", ""))

        if action == "refresh":
            return self.refreshChat(chatid)

        if action == "join":
            return self.joinChat()

        if action == "leave":
            return self.leaveChat(chatid)

        if action == "chatlist":
            return self.displayChatList()

        return self.displayChat()

    def getChatId(self, id):

        if id == 0 and self.AllianceId:
            id = self.request.session.get("alliancechat_" + str(self.AllianceId))

            if id == None or id == "":
                query = "SELECT chatid FROM alliances WHERE id=" + str(self.AllianceId)
                oRs = oConnExecute(query)

                if oRs:
                    self.request.session["alliancechat_" + str(self.AllianceId)] = oRs[0]
                    return oRs[0]
                    
        return id

    def addLine(self, chatid, msg):
        msg = msg.strip()[:260]
        if msg != "":
            connExecuteRetryNoRecords("INSERT INTO chat_lines(chatid, allianceid, userid, username, message) VALUES(" + str(chatid) + "," + str(sqlValue(self.AllianceId)) + "," + str(self.UserId) + "," + dosql(self.oPlayerInfo["username"]) + "," + dosql(msg) + ")")
        return HttpResponse(" ")

    def refreshContent(self, chatid):
        if chatid != 0 and self.request.session.get("chat_joined_" + str(chatid)) != "1": return HttpResponse(" ")

        userChatId = chatid

        chatid = self.getChatId(chatid)

        refresh_userlist = True

        lastmsgid = self.request.session.get("lastchatmsg_" + str(chatid), "")
        if lastmsgid == "": lastmsgid = 0

        query = "SELECT chat_lines.id, datetime, allianceid, username, message" + \
                " FROM chat_lines" + \
                " WHERE chatid=" + str(chatid) + " AND chat_lines.id > GREATEST((SELECT id FROM chat_lines WHERE chatid="+ str(chatid) +" ORDER BY datetime DESC OFFSET 100 LIMIT 1), " + str(lastmsgid) + ")" + \
                " ORDER BY chat_lines.id"
        oRss = oConnExecuteAll(query)

        if oRss == None: oRss = None

        # if there's no line to send and no list of users to send, exit
        if oRss == None and not refresh_userlist:
            return HttpResponse(" ") # return an empty string : fix safari "undefined XMLHttpRequest.status" bug

        # load the template

        content = getTemplate(self.request, "s03/chat-handler")
        content.setValue("username", self.oPlayerInfo["username"])
        content.setValue("chatid", userChatId)

        if oRss:
            list = []
            content.setValue("lines", list)
            for oRs in oRss:
                item = {}
                list.append(item)
                
                self.request.session["lastchatmsg_" + str(chatid)] = oRs[0]

                item["lastmsgid"] = oRs[0]
                item["datetime"] = oRs[1]
                item["author"] = oRs[3]
                item["line"] = oRs[4]
                item["alliancetag"] = getAllianceTag(oRs[2])

        # update user lastactivity in the DB and retrieve users online only every 3 minutes
        if refresh_userlist:

            # retrieve online users in chat
            query = "SELECT users.alliance_id, users.username, date_part('epoch', now()-chat_onlineusers.lastactivity)" + \
                    " FROM chat_onlineusers" + \
                    "    INNER JOIN users ON (users.id=chat_onlineusers.userid)" + \
                    " WHERE chat_onlineusers.lastactivity > now()-INTERVAL '10 minutes' AND chatid=" + str(chatid)
            oRss = oConnExecuteAll(query)

            list = []
            content.setValue("online_users", list)
            for oRs in oRss:
                item = {}
                list.append(item)
                
                item["alliancetag"] = getAllianceTag(oRs[0])
                item["user"] = oRs[1]
                item["lastactivity"] = oRs[2]

        content.Parse("refresh")

        return render(self.request, content.template, content.data)

    def refreshChat(self, chatid):
        return self.refreshContent(chatid)

    def displayChatList(self):

        content = getTemplate(self.request, "s03/chat-handler")
        content.setValue("username", self.oPlayerInfo["username"])

        query = "SELECT name, topic, count(chat_onlineusers.userid)" + \
                " FROM chat" + \
                "    LEFT JOIN chat_onlineusers ON (chat_onlineusers.chatid = chat.id AND chat_onlineusers.lastactivity > now()-INTERVAL '10 minutes')" + \
                " WHERE name IS NOT NULL AND password = \'\' AND public" + \
                " GROUP BY name, topic" + \
                " ORDER BY length(name), name"
        oRss = oConnExecuteAll(query)

        list = []
        content.setValue("publicchats", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["name"] = oRs[0]
            item["topic"] = oRs[1]
            item["online"] = oRs[2]

        return render(self.request, content.template, content.data)

    # add a chat to the joined chat list
    def addChat(self, chatid):
        result = True

        #self.request.session["lastchatactivity_" + str(chatid)] = timezone.now()-self.onlineusers_refreshtime

        if self.request.session.get("chat_joined_" + str(chatid)) != "1":
            self.request.session["chat_joined_count"] = ToInt(self.request.session.get("chat_joined_count"), 0) + 1
            self.request.session["chat_joined_" + str(chatid)] = "1"

            result = True
        
        return result

    # remove a chat from list
    def removeChat(self, chatid):
        if self.request.session.get("chat_joined_" + str(chatid)) == "1":
            self.request.session["chat_joined_" + str(chatid)] = ""
            self.request.session["chat_joined_count"] = self.request.session.get("chat_joined_count") - 1

    def displayChat(self):
        self.request.session["chatinstance"] = ToInt(self.request.session.get("chatinstance"), 0) + 1

        content = getTemplate(self.request, "s03/chat")
        content.setValue("username", self.oPlayerInfo["username"])
        content.setValue("chatinstance", self.request.session.get("chatinstance"))

        if (self.AllianceId):
            chatid = self.getChatId(0)
            self.request.session["lastchatmsg_" + str(chatid)] = ""
            #self.request.session["lastchatactivity_" + str(chatid)] = str(timezone.now()-timezone.timedelta(seconds=self.onlineusers_refreshtime))

            content.Parse("alliance")

        query = "SELECT chat.id, chat.name, chat.topic" + \
                " FROM users_chats" + \
                "    INNER JOIN chat ON (chat.id=users_chats.chatid AND ((chat.password = '') OR (chat.password = users_chats.password)))" + \
                " WHERE userid = " + str(self.UserId) + \
                " ORDER BY users_chats.added"
        oRss = oConnExecuteAll(query)

        list = []
        content.setValue("joins", list)
        for oRs in oRss:
            if self.addChat(oRs[0]):
                item = {}
                list.append(item)
                
                item["id"] = oRs[0]
                item["name"] = oRs[1]
                item["topic"] = oRs[2]

                self.request.session["lastchatmsg_" + str(oRs[0])] = ""

        content.setValue("now", timezone.now())

        content.Parse("chat")

        return self.display(content)

    def joinChat(self):

        content = getTemplate(self.request, "s03/chat-handler")
        content.setValue("username", self.oPlayerInfo["username"])

        pwd = self.request.GET.get("pass", "").strip()

        # join chat
        query = "SELECT sp_chat_join(" + dosql(self.request.GET.get("chat", "").strip()) + "," + dosql(pwd) + ")"
        oRs = oConnExecute(query)

        chatid = oRs[0]

        if not self.addChat(oRs[0]): return

        if chatid != 0:
            # save the chatid to the user chatlist
            query = "INSERT INTO users_chats(userid, chatid, password) VALUES(" + str(self.UserId) + "," + str(chatid) + "," + dosql(pwd) + ")"
            oConnDoQuery(query)

            query = "SELECT name, topic FROM chat WHERE id=" + str(chatid)
            oRs = oConnExecute(query)

            if oRs:
                content.setValue("id", chatid)
                content.setValue("name", oRs[0])
                content.setValue("topic", oRs[1])
                content.Parse("setactive")
                content.Parse("join")

                self.request.session["lastchatmsg_" + str(chatid)] = ""

            else:
                content.Parse("join_error")

        else:
            content.Parse("join_badpassword")

        return render(self.request, content.template, content.data)

    def leaveChat(self, chatid):
        self.request.session["lastchatmsg_" + str(chatid)] = ""

        self.removeChat(chatid)

        query = "DELETE FROM users_chats WHERE userid=" + str(self.UserId) + " AND chatid=" + str(chatid)
        oConnDoQuery(query)

        query = "DELETE FROM chat WHERE id > 0 AND NOT public AND name IS NOT NULL AND id=" + str(chatid) + " AND (SELECT count(1) FROM users_chats WHERE chatid=chat.id) = 0"
        oConnDoQuery(query)
        
        return HttpResponse(" ")
