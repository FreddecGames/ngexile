# -*- coding: utf-8 -*-

from myapps.s03.views._global import *

from myapps.s03.views._utils import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selectedMenu = "notes"

        self.notes_status = ""

        notes = request.POST.get("notes", "").strip()

        if request.POST.get("submit", "") != "":

            if len(notes) <= 5100: # ok save info
                oConnDoQuery("UPDATE users SET notes=" + dosql(notes) + " WHERE id = " + str(self.userId))
                self.notes_status = "done"
            else:
                self.notes_status = "toolong"

        return self.display_notes()

    def display_notes(self):

        content = getTemplate(self.request, "s03/notes")

        content.setValue("maxlength", 5000)

        oRs = oConnExecute("SELECT notes FROM users WHERE id = " + str(self.userId) + " LIMIT 1" )

        content.setValue("data_notes", oRs[0])

        if self.notes_status != "":
            content.Parse(self.notes_status)
            content.Parse("error")

        return self.display(content)
