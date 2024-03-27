# -*- coding: utf-8 -*-

from myapps.api.views._utils import *

#---

class View(BaseView):

    def get(self, request, format=None):
        
        query = 'SELECT username, privilege, resets, credits, lastplanetid, deletion_date, planets, score, previous_score, mod_planets, mod_commanders,' + \
                ' alliance_id, alliance_rank, leave_alliance_datetime IS NULL AND (alliance_left IS NULL OR alliance_left < now()) AS can_join_alliance,' + \
                ' credits_bankruptcy, orientation, prestige_points' + \
                ' FROM users' + \
                ' WHERE id=' + str(self.userId)
        
        data = dbRow(query)
        return Response(data)
