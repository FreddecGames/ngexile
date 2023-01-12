from .base import *

class View(GlobalView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response

        self.selected_menu = "alliance"

        self.name = ""
        self.tag = ""
        self.description = ""

        self.valid_name = True
        self.valid_tag = True
        self.valid_description = True
        self.create_result = 0

        if request.GET.get("a") == "new":
            self.name = request.POST.get("alliancename", "").strip()
            self.tag = request.POST.get("alliancetag", "").strip()
            self.description = request.POST.get("description", "").strip()

            self.valid_name = self.isValidAlliancename(self.name)
            self.valid_tag = self.isValidAlliancetag(self.tag)
            self.valid_description = self.isValiddescription(self.description)

            if self.valid_name and self.valid_tag and self.valid_description:

                oRs = oConnExecute("SELECT sp_create_alliance(" + str(self.UserId) + "," + dosql(self.name) + "," + dosql(self.tag) + "," + dosql(self.description) + ")")

                self.create_result = oRs[0]
                if self.create_result >= -1:
                    return HttpResponseRedirect("/s03/alliance-view/")

        content = GetTemplate(self.request, "alliance-create")

        if self.oPlayerInfo["can_join_alliance"]:
            if self.create_result == -2: content.Parse("name_already_used")
            if self.create_result == -3: content.Parse("tag_already_used")

            if not self.valid_name: content.Parse("invalid_name")

            if not self.valid_tag: content.Parse("invalid_tag")

            content.AssignValue("name", self.name)
            content.AssignValue("tag", self.tag)
            content.AssignValue("description", self.description)

            content.Parse("create")
        else:
            content.Parse("cant_create")

        return self.Display(content)

    #
    # return if the given self.name is valid for an alliance
    #
    def isValidAlliancename(self, myname):

        if myname == "" or len(myname) < 4 or len(myname) > 32:
            return False
        else:
            p = re.compile("^[a-zA-Z0-9]+([ ]?[.]?[\-]?[ ]?[a-zA-Z0-9]+)*$")
            return p.match(myname)

    #
    # return if the given self.tag is valid
    #
    def isValidAlliancetag(self, tag):

        if tag == "" or len(tag) < 2 or len(tag) > 4:
            return False
        else:
            p = re.compile("^[a-zA-Z0-9]+$")
            return p.match(tag)

    def isValiddescription(self, description):
        return len(description) < 8192
