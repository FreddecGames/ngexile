# -*- coding: utf-8 -*-

from ._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "fleets.fleets"

        return self.DisplayFleetsPage()

    def DisplayFleetsPage(self):

        content = GetTemplate(self.request, "fleets")

        query = "SELECT category, label" + \
                " FROM users_fleets_categories" + \
                " WHERE userid=" + str(self.UserId) + \
                " ORDER BY upper(label)"
        oRss = oConnExecuteAll(query)

        list = []
        content.AssignValue("categories", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["id"] = oRs[0]
            item["label"] = oRs[1]

        content.Parse("master")

        return self.Display(content)

