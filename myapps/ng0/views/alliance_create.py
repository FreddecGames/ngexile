from .base import *

class View(BaseView):

    def dispatch(self, request, *args, **kwargs):

        response = super().pre_dispatch(request, *args, **kwargs)
        if response: return response
        
        #--- post

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

            self.valid_name = isValidAlliancename(self.name)
            self.valid_tag = isValidAlliancetag(self.tag)
            self.valid_description = isValiddescription(self.description)

            if self.valid_name and self.valid_tag and self.valid_description:

                oRs = oConnExecute("SELECT sp_create_alliance(" + str(self.profile['id']) + "," + strSql(self.name) + "," + strSql(self.tag) + "," + strSql(self.description) + ")")

                self.create_result = oRs[0]
                if self.create_result >= -1:
                    return HttpResponseRedirect("/s03/alliance-view/")
        
        #--- get

        self.selectedMenu = "alliance"

        content = getTemplateContext(self.request, "alliance-create")

        if self.oPlayerInfo["can_join_alliance"]:
            if self.create_result == -2: content.parse("name_already_used")
            if self.create_result == -3: content.parse("tag_already_used")

            if not self.valid_name: content.parse("invalid_name")

            if not self.valid_tag: content.parse("invalid_tag")

            content.assignValue("name", self.name)
            content.assignValue("tag", self.tag)
            content.assignValue("description", self.description)

            content.parse("create")
        else:
            content.parse("cant_create")

        return self.display(content)
