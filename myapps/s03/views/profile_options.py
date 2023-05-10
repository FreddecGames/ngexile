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
    
        if request.POST.get("submit", "") != "":
            
            optionCat = ToInt(request.GET.get("cat"), 1)
            if optionCat == 1:
                
                avatar = request.POST.get("avatar", "").strip()
                description = request.POST.get("description", "").strip()
            
                if avatar != "" and not isValidURL(avatar): messages.error(request, 'check_avatar')
                else:
                    
                    query = "UPDATE users SET" + \
                            " avatar_url=" + dosql(avatar) + ", description=" + dosql(description) + \
                            " WHERE id=" + str(self.userId)
                    dbQuery(query)

            elif optionCat == 2:
            
                score_visibility = ToInt(request.POST.get("score_visibility"), 0)
                if score_visibility < 0 or score_visibility > 2: score_visibility = 0

                deletingaccount = request.POST.get("deleting")
                deleteaccount = request.POST.get("delete")

                query = "UPDATE users SET score_visibility=" + str(score_visibility)
                if deletingaccount and not deleteaccount: query = query + ", deletion_date=NULL"
                if not deletingaccount and deleteaccount: query = query + ", deletion_date=now() + INTERVAL '2 days'"
                query = query + " WHERE id=" + str(self.userId)
                dbQuery(query)
                
            elif optionCat == 3 and request.POST.get("holidays"):
            
                result = dbRow("SELECT COALESCE(int4(date_part('epoch', now()-last_holidays)), 10000000) AS cooldown, (SELECT 1 FROM users_holidays WHERE userid=users.id) AS holidays FROM users WHERE id=" + str(self.userId))
                if result['cooldown'] > (7 * 24 * 60 * 60) and result['holidays'] == None:
                
                    query = "INSERT INTO users_holidays(userid, start_time, min_end_time, end_time) VALUES(" + str(self.userId) + ",now()+INTERVAL '24 hours', now()+INTERVAL '72 hours', now()+INTERVAL '22 days')"
                    dbQuery(query)
            
        #---
        
        return HttpResponseRedirect(request.build_absolute_uri())
            
    def get(self, request, *args, **kwargs):
    
        content = getTemplate(request, "s03/options")
        
        self.selectedMenu = "options"

        #---

        optionCat = ToInt(request.GET.get("cat"), 1)
        if optionCat < 1 or optionCat > 3: optionCat = 1
        content.setValue("cat", optionCat)

        #---
        
        if optionCat == 1:
        
            query = "SELECT avatar_url, regdate, users.description, 0," + \
                    " alliance_id, a.tag, a.name, r.label" + \
                    " FROM users" + \
                    " LEFT JOIN alliances AS a ON (users.alliance_id = a.id)" + \
                    " LEFT JOIN alliances_ranks AS r ON (users.alliance_id = r.allianceid AND users.alliance_rank = r.rankid) " + \
                    " WHERE users.id = " + str(self.userId)
            row = dbRow(query)
            content.setValue("profile", row)

        #---
        
        elif optionCat == 2:
        
            row = dbRow("SELECT int4(date_part('epoch', deletion_date-now())) AS remainingtime, score_visibility FROM users WHERE id=" + str(self.userId))
            content.setValue("data", row)

        #---
        
        elif optionCat == 3:
        
            result = dbExecute("SELECT int4(date_part('epoch', start_time-now())) AS remainingtime FROM users_holidays WHERE userid=" + str(self.userId))
            content.setValue("start_in", result)

            if not result or result <= 0:
            
                result = dbExecute("SELECT int4(date_part('epoch', now()-last_holidays)) FROM users WHERE id=" + str(self.userId))
                if result and result < (7 * 24 * 60 * 60):
                
                    content.setValue("remaining_time", (7 * 24 * 60 * 60) - result)
                    content.Parse("cant_enable")
                    
                else: content.Parse("can_enable")
                
        #---
        
        return self.display(content, request)
