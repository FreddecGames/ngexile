from .base import *


class View(BaseView):

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
            oConnExecute("SELECT sp_ignore_sender(" + str(self.profile['id']) + "," + strSql(request.GET.get("user")) + ")")

        if request.GET.get("a", "") == "unignore":
            dbQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.profile['id']) + " AND ignored_userid=(SELECT id FROM users WHERE lower(username)=lower(" + strSql(request.GET.get("user")) + "))")

        if request.GET.get("a") == "unignorelist":
            for self.mailto in request.POST.getlist("unignore"):
                dbQuery("DELETE FROM messages_ignore_list WHERE userid=" + str(self.profile['id']) + " AND ignored_userid=" + strSql(self.mailto))

        self.selectedMenu = "mails"

        content = getTemplateContext(self.request, "mail-blacklist")

        oRss = oConnExecuteAll("SELECT ignored_userid, sp_get_user(ignored_userid), added, blocked FROM messages_ignore_list WHERE userid=" + str(self.profile['id']))

        i = 0
        list = []
        content.assignValue("ignorednations", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["index"] = i
            item["userid"] = oRs[0]
            item["name"] = oRs[1]
            item["added"] = oRs[2]
            item["blocked"] = oRs[3]

            i = i + 1

        if i == 0: content.parse("noignorednations")

        return self.display(content)
