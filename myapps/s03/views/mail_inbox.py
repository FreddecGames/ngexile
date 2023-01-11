from .base import *


class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "mails"

        self.compose = False
        self.mailto = ""
        self.mailsubject = ""
        self.mailbody = ""
        self.moneyamount = 0
        self.bbcode = False
        self.sendmail_status = ""

        # new email
        if request.POST.get("compose", "") != "":
            self.compose = True
        elif request.GET.get("to", "") != "":
            self.mailto = request.GET.get("to", "")
            self.mailsubject = request.GET.get("subject", "")
            self.compose = True
        elif request.GET.get("a", "") == "new":

            self.mailto = request.GET.get("b", "")
            if self.mailto == "": self.mailto = request.GET.get("to", "")
            self.mailsubject = request.GET.get("subject", "")
            self.compose = True

        # reply
        elif request.GET.get("a", "") == "reply":

            Id = ToInt(request.GET.get("mailid"), 0)

            query = "SELECT sender, subject, body FROM messages WHERE ownerid=" + str(self.UserId) + " AND id=" + str(Id) + " LIMIT 1"
            oRs = oConnExecute(query)

            if oRs:

                self.mailto = oRs[0]

                # adds 'Re: # to new reply

                if "Re:" in oRs[1]:
                    self.mailsubject = oRs[1]
                else:
                    self.mailsubject = "Re: " + oRs[1]

                self.mailbody = self.quote_mail("> " + oRs[2] + "\n")

                self.compose = True

        # send email
        elif request.POST.get("sendmail", "") != "" and not self.IsImpersonating():

            self.compose = True

            self.mailto = request.POST.get("to", "").strip()
            self.mailsubject = request.POST.get("subject", "").strip()
            self.mailbody = request.POST.get("message", "").strip()

            if ToInt(request.POST.get("sendcredits"), 0) == 1:
                self.moneyamount = ToInt(request.POST.get("amount"), 0)
            else:
                self.moneyamount = 0

            self.bbcode = request.POST.get("self.bbcode") == 1

            if self.mailbody == "":
                self.sendmail_status = "mail_empty"
            else:
                if request.POST.get("type") == "admins":
                    self.mailto = ":admins"
                    self.moneyamount = 0
                elif request.POST.get("type") == "alliance":
                    # send the mail to all members of the alliance except
                    self.mailto = ":alliance"
                    self.moneyamount = 0

                if self.mailto == "":
                    self.sendmail_status = "mail_missing_to"
                else:
                    oRs = oConnExecute("SELECT sp_send_message("+ str(self.UserId) + "," + dosql(self.mailto) + "," + dosql(self.mailsubject) + "," + dosql(self.mailbody) + "," + str(self.moneyamount) + "," + str(self.bbcode) + ")")

                    if oRs[0] != 0:
                        if oRs[0] == 1:
                            self.sendmail_status = "mail_unknown_from" # from not found
                        elif oRs[0] == 2:
                            self.sendmail_status = "mail_unknown_to" # to not found
                        elif oRs[0] == 3:
                            self.sendmail_status = "mail_same" # send to same person
                        elif oRs[0] == 4:
                            self.sendmail_status = "not_enough_credits" # not enough credits
                        elif oRs[0] == 9:
                            self.sendmail_status = "blocked" # messages are blocked

                    else:
                        self.sendmail_status = "mail_sent"

                        self.mailsubject = ""
                        self.mailbody = ""
                        self.moneyamount = 0

        # delete selected emails
        elif request.POST.get("delete", "") != "":

            # build the query of which mails to delete
            query = "False"

            for mailid in request.POST.getlist("checked_mails"):
                print(mailid)
                query = query + " OR id=" + mailid

            if query != "False":
                oConnDoQuery("UPDATE messages SET deleted=True WHERE (" + query + ") AND ownerid = " + str(self.UserId))
        
        if request.GET.get("a", "") == "ignore":
            print(dosql(request.GET.get("user")))
            oConnExecute("SELECT sp_ignore_sender(" + str(self.UserId) + "," + dosql(request.GET.get("user")) + ")")

            return self.display_mails()

        if request.GET.get("a", "") == "unignore":
            oConnDoQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.UserId) + " AND ignored_userid=(SELECT id FROM users WHERE lower(username)=lower(" + dosql(request.GET.get("user")) + "))")

            return self.display_mails()

        if self.compose:
            return self.display_compose_form(self.mailto, self.mailsubject, self.mailbody, self.moneyamount)
        elif request.GET.get("a") == "ignorelist":
            return self.display_ignore_list()
        elif request.GET.get("a") == "unignorelist":
            for self.mailto in request.POST.getlist("unignore"):
                oConnDoQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.UserId) + " AND ignored_userid=" + dosql(self.mailto))

            return self.display_ignore_list()
        elif request.GET.get("a") == "sent":
            return self.display_mails_sent()
        else:
            return self.display_mails()
    #
    # display mails received by the player
    #
    def display_mails(self):

        self.selected_menu = "mails"

        content = GetTemplate(self.request, "mail-inbox")

        displayed = 30 # number of messages displayed per page

        #
        # Retrieve the offset from where to begin the display
        #
        offset = ToInt(self.request.GET.get("start"), 0)
        if offset > 50: offset=50
        if offset < 0: offset=0

        # get total number of mails that could be displayed
        query = "SELECT count(1) FROM messages WHERE NOT deleted AND ownerid = " + str(self.UserId)
        oRs = oConnExecute(query)
        size = int(oRs[0])
        nb_pages = int(size/displayed)
        if nb_pages*displayed < size: nb_pages = nb_pages + 1
        if offset >= nb_pages: offset = nb_pages-1

        if offset < 0: offset=0
        content.AssignValue("offset", offset)

        if nb_pages > 50: nb_pages=50

        #display all links only if there are a few pages
        list = []
        content.AssignValue("ps", list)
        for i in range(1, nb_pages+1):
            item = {}
            list.append(item)
            
            item["page_id"] = i
            item["page_link"] = i-1

            if i != offset+1:
                item["link"] = True
            else:
                item["selected"] = True

            item["offset"] = offset

        content.AssignValue("min", offset*displayed+1)
        if offset+1 == nb_pages:
            content.AssignValue("max", size)
        else:
            content.AssignValue("max", (offset+1)*displayed)

        content.AssignValue("page_display", offset+1)

        #display only if there are more than 1 page
        if nb_pages > 1: content.Parse("nav")

        query = "SELECT sender, subject, body, datetime, messages.id, read_date, avatar_url, users.id, messages.credits," + \
                " users.privilege, bbcode, owner, messages_ignore_list.added, alliances.tag"+ \
                " FROM messages" + \
                "    LEFT JOIN users ON (upper(users.username) = upper(messages.sender) AND messages.datetime >= users.game_started)" + \
                "    LEFT JOIN alliances ON (users.alliance_id = alliances.id)" + \
                "    LEFT JOIN messages_ignore_list ON (userid=" + str(self.UserId) + " AND ignored_userid = users.id)" + \
                " WHERE NOT deleted AND ownerid = " + str(self.UserId) + \
                " ORDER BY datetime DESC, messages.id DESC" + \
                " OFFSET " + str(offset*displayed) + " LIMIT "+str(displayed)
        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.AssignValue("mails", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["index"] = i
            item["from"] = oRs[0]
            item["subject"] = oRs[1]
            item["date"] = oRs[3]

            if oRs[10]:
                item["bodybb"] = oRs[2]
                item["bbcode"] = True
            else:
                item["body"] = oRs[2].replace("\n", "<br/>")
                item["html"] = True

            item["mailid"] = oRs[4]
            item["moneyamount"] = oRs[8]

            if oRs[8] > 0: item["money"] = True # sender has given money

            if oRs[9] and oRs[9] >= 500: item["from_admin"] = True

            if oRs[6] == None or oRs[6] == "":
                item["noavatar"] = True
            else:
                item["avatar_url"] = oRs[6]
                item["avatar"] = True

            if oRs[5] == None: item["new_mail"] = True # if there is no value for read_date: it is a new mail

            if oRs[7]:
                # allow the player to block/ignore another player
                if oRs[12]:
                    item["ignored"] = True
                else:
                    item["ignore"] = True

                if oRs[13]:
                    item["alliancetag"] = oRs[13]
                    item["alliance"] = True

                item["reply"] = True

            if oRs[11] == ":admins":
                item["to_admins"] = True
            elif oRs[11] == ":alliance":
                item["to_alliance"] = True

            i = i + 1

        if i == 0: content.Parse("nomails")

        if not self.IsImpersonating():
            oRs = oConnDoQuery("UPDATE messages SET read_date = now() WHERE ownerid = " + str(self.UserId) + " AND read_date IS NULL" )

        return self.Display(content)

    #
    # display mails sent by the player
    #
    def display_mails_sent(self):

        self.selected_menu = "mails"

        content = GetTemplate(self.request, "mail-outbox")

        displayed = 30 # number of nations displayed per page

        #
        # Retrieve the offset from where to begin the display
        #
        offset = ToInt(self.request.GET.get("start"), 0)
        if offset > 50: offset=50

        messages_filter = "datetime > now()-INTERVAL '2 weeks' AND "

        # get total number of mails that could be displayed
        query = "SELECT count(1) FROM messages WHERE "+messages_filter+"senderid = " + str(self.UserId)
        oRs = oConnExecute(query)
        size = int(oRs[0])
        nb_pages = int(size/displayed)
        if nb_pages*displayed < size: nb_pages = nb_pages + 1

        if nb_pages > 50: nb_pages=50

        #display all links only if there are a few pages
        list = []
        content.AssignValue("ps", list)
        for i in range(1, nb_pages+1):
            item = {}
            list.append(item)
            
            item["page_id"] = i
            item["page_link"] = i-1

            if i != offset+1:
                item["link"] = True
            else:
                item["selected"] = True

            item["offset"] = offset

        content.AssignValue("min", offset*displayed+1)
        if offset+1 == nb_pages:
            content.AssignValue("max", size)
        else:
            content.AssignValue("max", (offset+1)*displayed)

        content.AssignValue("page_display", offset+1)

        #display only if there are more than 1 page
        if nb_pages > 1: content.Parse("nav")

        query = "SELECT messages.id, owner, avatar_url, datetime, subject, body, messages.credits, users.id, bbcode, alliances.tag"+ \
                " FROM messages" + \
                "    LEFT JOIN users ON (/*upper(users.username) = upper(messages.owner)*/ users.id = messages.ownerid AND messages.datetime >= users.game_started)" + \
                "    LEFT JOIN alliances ON (users.alliance_id = alliances.id)" + \
                " WHERE "+messages_filter+"senderid = " + str(self.UserId) + \
                " ORDER BY datetime DESC"

        query = query + " OFFSET "+str(offset*displayed)+" LIMIT "+str(displayed)

        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.AssignValue("mails", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["index"] = i
            item["sent_to"] = oRs[1]

            if oRs[1] == ":admins":
                item["admins"] = True
            elif oRs[1] == ":alliance":
                item["to_alliance"] = True
            else:
                item["nation"] = True

            item["date"] = oRs[3]
            item["subject"] = oRs[4]

            if oRs[8]:
                item["bodybb"] = oRs[5]
                item["bbcode"] = True
            else:
                item["body"] = oRs[5].replace("\n", "<br/>")
                item["html"] = True

            item["mailid"] = oRs[0]
            item["moneyamount"] = oRs[6]

            if oRs[6] > 0: # sender has given money
                item["money"] = True

            if oRs[2] == None or oRs[2] == "":
                item["noavatar"] = True
            else:
                item["avatar_url"] = oRs[2]
                item["avatar"] = True

            if oRs[7]:
                if oRs[9]:
                    item["alliancetag"] = oRs[9]
                    item["alliance"] = True

                item["reply"] = True

            i = i + 1

        if i == 0: content.Parse("nomails")

        return self.Display(content)

    def display_ignore_list(self):
        self.selected_menu = "mails"

        content = GetTemplate(self.request, "mail-blacklist")

        oRss = oConnExecuteAll("SELECT ignored_userid, sp_get_user(ignored_userid), added, blocked FROM messages_ignore_list WHERE userid=" + str(self.UserId))

        i = 0
        list = []
        content.AssignValue("ignorednations", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["index"] = i
            item["userid"] = oRs[0]
            item["name"] = oRs[1]
            item["added"] = oRs[2]
            item["blocked"] = oRs[3]

            i = i + 1

        if i == 0: content.Parse("noignorednations")

        return self.Display(content)

    def return_ignored_users(self):

        content = GetTemplate(self.request, "mail-inbox")

        oRss = oConnExecuteAll("SELECT sp_get_user(ignored_userid) FROM messages_ignore_list WHERE userid=" + userid)
        list = []
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["user"] = oRs[0]
            content.Parse("ignored_user")

        response.write(content.Output)

    # quote reply
    def quote_mail(self, body):

        self.sendmail_status=""
        return body.replace("\n", "\n" + "> ") + "\n\n"

    # fill combobox with previously sent to
    def display_compose_form(self, mailto, subject, body, credits):

        self.selected_menu = "mails"

        content = GetTemplate(self.request, "mail-new")

        # fill the recent addressee list

        oRss = oConnExecuteAll("SELECT * FROM sp_get_addressee_list(" + str(self.UserId) + ")")

        list = []
        content.AssignValue("tos", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["to_user"] = oRs[0]

        if self.mailto == ":admins":
            content.Parse("sendadmins_selected")

            content.Parse("hidenation")
            content.Parse("send_credits_hide")
            self.mailto = ""
        elif self.mailto == ":alliance":
            content.Parse("sendalliance_selected")

            content.Parse("hidenation")
            content.Parse("send_credits_hide")
            self.mailto = ""
        else:
            content.Parse("nation_selected")

        if (self.oAllianceRights):
            if self.oAllianceRights["can_mail_alliance"]: content.Parse("sendalliance")

        # if is a payed account, append the autosignature text to message body
        if self.oPlayerInfo["paid"]:
            oRs = oConnExecute("SELECT autosignature FROM users WHERE id="+userid)
            if oRs:
                body = body  + oRs[0]

        # re-assign previous values
        content.AssignValue("mailto", mailto)
        content.AssignValue("subject", subject)
        content.AssignValue("message", body)
        content.AssignValue("mail_credits", credits)

        #retrieve player's credits
        oRs = oConnExecute("SELECT credits, now()-game_started > INTERVAL '2 weeks' AND security_level >= 3 FROM users WHERE id="+str(self.UserId))
        content.AssignValue("player_credits", oRs[0])
        if oRs[1]: content.Parse("send_credits")

        if self.sendmail_status != "":
            content.Parse(self.sendmail_status)
            content.Parse("error")

        if self.bbcode: content.Parse("bbcode")

        self.FillHeaderCredits(content)

        return self.Display(content)
