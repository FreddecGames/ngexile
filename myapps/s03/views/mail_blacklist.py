from .base import *


class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "mails"

        self.compose = False
        self.mailto = ""
        self.mailsubject = ""
        self.mailbody = ""
        self.moneyamount = 0
        self.bbcode = False
        self.sendmail_status = ""

        if request.GET.get("a", "") == "ignore":
            oConnExecute("SELECT sp_ignore_sender(" + str(self.UserId) + "," + dosql(request.GET.get("user")) + ")")

        if request.GET.get("a", "") == "unignore":
            oConnDoQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.UserId) + " AND ignored_userid=(SELECT id FROM users WHERE lower(username)=lower(" + dosql(request.GET.get("user")) + "))")

        if request.GET.get("a") == "unignorelist":
            for self.mailto in request.POST.getlist("unignore"):
                oConnDoQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.UserId) + " AND ignored_userid=" + dosql(self.mailto))

        self.selectedMenu = "mails"

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
