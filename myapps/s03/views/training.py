# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "planet"

        self.showHeader = True

        self.train_error = 0

        Action = request.GET.get("a", "").lower()
        trainScientists = ToInt(request.POST.get("scientists"),0)
        trainSoldiers = ToInt(request.POST.get("soldiers"),0)
        queueId = ToInt(request.GET.get("q"),0)

        if Action == "train":
            self.Train(trainScientists, trainSoldiers)
        elif Action == "cancel":
            self.CancelTraining(queueId)

        return self.DisplayTraining()

    def DisplayTraining(self):

        content = getTemplate(self.request, "s03/training")

        content.setValue("planetid", str(self.CurrentPlanet))

        query = "SELECT scientist_ore, scientist_hydrocarbon, scientist_credits," + \
                " soldier_ore, soldier_hydrocarbon, soldier_credits" + \
                " FROM sp_get_training_price(" + str(self.UserId) + ")"
        oRs = oConnExecute(query)

        if oRs:
            content.setValue("scientist_ore", oRs[0])
            content.setValue("scientist_hydrocarbon", oRs[1])
            content.setValue("scientist_credits", oRs[2])
            content.setValue("soldier_ore", oRs[3])
            content.setValue("soldier_hydrocarbon", oRs[4])
            content.setValue("soldier_credits", oRs[5])

        query = "SELECT scientists, scientists_capacity, soldiers, soldiers_capacity, workers FROM vw_planets WHERE id="+str(self.CurrentPlanet)
        oRs = oConnExecute(query)

        if oRs:
            content.setValue("scientists", oRs[0])
            content.setValue("scientists_capacity", oRs[1])

            content.setValue("soldiers", oRs[2])
            content.setValue("soldiers_capacity", oRs[3])
            if oRs[2]*250 < oRs[0]+oRs[4]: content.Parse("not_enough_soldiers")

            if oRs[0] < oRs[1]:
                content.Parse("input_scientists")
            else:
                content.Parse("max_scientists")

            if oRs[2] < oRs[3]:
                content.Parse("input_soldiers")
            else:
                content.Parse("max_soldiers")

        if self.train_error != 0:
            if self.train_error == 5: content.Parse("cant_train_now")
            else: content.Parse("not_enough_workers")

            content.Parse("error")

        # training in process
        query = "SELECT id, scientists, soldiers, int4(date_part('epoch', end_time-now()))" + \
                " FROM planet_training_pending WHERE planetid="+str(self.CurrentPlanet)+" AND end_time IS NOT NULL" + \
                " ORDER BY start_time"
        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.setValue("trainings", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["queueid"] = oRs[0]
            item["remainingtime"] = oRs[3]

            if oRs[1] > 0:
                item["quantity"] = oRs[1]
                item["scientists"] = True

            if oRs[2] > 0:
                item["quantity"] = oRs[2]
                item["soldiers"] = True

            i = i + 1

        # queue
        query = "SELECT planet_training_pending.id, planet_training_pending.scientists, planet_training_pending.soldiers," + \
                "    int4(ceiling(1.0*planet_training_pending.scientists/GREATEST(1, training_scientists)) * date_part('epoch', INTERVAL '1 hour'))," + \
                "    int4(ceiling(1.0*planet_training_pending.soldiers/GREATEST(1, training_soldiers)) * date_part('epoch', INTERVAL '1 hour'))" + \
                " FROM planet_training_pending" + \
                "    JOIN nav_planet ON (nav_planet.id=planet_training_pending.planetid)" + \
                " WHERE planetid="+str(self.CurrentPlanet)+" AND end_time IS NULL" + \
                " ORDER BY start_time"
        oRss = oConnExecuteAll(query)

        i = 0
        list = []
        content.setValue("queues", list)
        for oRs in oRss:
            item = {}
            list.append(item)
            
            item["queueid"] = oRs[0]

            if oRs[1] > 0:
                item["quantity"] = oRs[1]
                item["remainingtime"] = oRs[3]
                item["scientists"] = True

            if oRs[2] > 0:
                item["quantity"] = oRs[2]
                item["remainingtime"] = oRs[4]
                item["soldiers"] = True

            i = i + 1

        return self.display(content)

    def Train(self, Scientists, Soldiers):

        oRs = connExecuteRetry("SELECT * FROM sp_start_training(" + str(self.UserId) + "," + str(self.CurrentPlanet) + "," + str(Scientists) + "," + str(Soldiers) + ")")

        if oRs:
            self.train_error = oRs[0]
        else:
            self.train_error = 1

    def CancelTraining(self, queueId):
        connExecuteRetryNoRecords("SELECT * FROM sp_cancel_training(" + str(self.CurrentPlanet) + ", " + str(queueId) + ")")
        return HttpResponseRedirect("?")

