from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "ranking"

        content = GetTemplate(self.request, "ranking-players")

        query = "SELECT username, v.score, v.score_prestige," + \
                "COALESCE(date_part('day', now()-lastactivity), 15), alliances.name, alliances.tag, v.id, avatar_url, v.alliance_id, v.score-v.previous_score AS score_delta," + \
                "score_visibility = 2 OR (score_visibility = 1 AND alliance_id IS NOT NULL AND alliance_id="+str(sqlValue(self.AllianceId))+") OR v.id="+str(self.UserId) + \
                " FROM vw_players v" + \
                "    LEFT JOIN alliances ON ((score_visibility = 2 OR v.id="+str(self.UserId)+" OR (score_visibility = 1 AND alliance_id IS NOT NULL AND alliance_id="+str(sqlValue(self.AllianceId))+")) AND alliances.id=v.alliance_id)" + \
                " ORDER BY v.score DESC"
        oRss = oConnExecuteAll(query)

        i = 1
        list = []
        content.AssignValue("players", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["place"] = i
            item["username"] = oRs[0]

            visible = oRs[10]

            if visible and oRs[4]:
                item["alliancename"] = oRs[4]
                item["alliancetag"] = oRs[5]
                item["alliance"] = True
            else:
                item["noalliance"] = True

            item["score"] = oRs[1]
            item["score_battle"] = oRs[2]
            if visible:
                item["score_delta"] = oRs[9]
                if oRs[9] > 0: item["plus"] = True
                if oRs[9] < 0: item["minus"] = True
            else:
                item["score_delta"] = ""

            item["stat_colonies"] = oRs[2]
            item["last_login"] = oRs[3]

            if oRs[3] <= 7:
                item["recently"] = True
            elif oRs[3] <= 14:
                item["1weekplus"] = True
            elif oRs[3] > 14:
                item["2weeksplus"] = True

            if visible:
                if oRs[6] == self.UserId:
                    item["self"] = True
                elif self.AllianceId and oRs[8] == self.AllianceId:
                    item["ally"] = True

                # show avatar only if top 10
                if oRs[7] == None or oRs[7] == "":
                    item["noavatar"] = True
                else:
                    item["avatar_url"] = oRs[7]
                    item["avatar"] = True

                item["name"] = True
            else:
                item["name_na"] = True

            i = i + 1

        return self.Display(content)
