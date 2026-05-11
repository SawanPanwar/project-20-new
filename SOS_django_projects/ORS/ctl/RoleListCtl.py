from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.RoleService import RoleService


class RoleListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["name"] = requestForm.get("name", None)
        self.form["description"] = requestForm.get("description", None)

    def display(self, request, params={}):
        RoleListCtl.count = self.form['pageNo']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {"form": self.form, "pageList": self.page_list})
        return res

    def submit(self, request, params={}):
        self.form['pageNo'] = RoleListCtl.count
        if request.POST['operation'] == "Next":
            RoleListCtl.count += 1
            self.form['pageNo'] = RoleListCtl.count
        if request.POST['operation'] == "Previous":
            RoleListCtl.count -= 1
            self.form['pageNo'] = RoleListCtl.count
        if request.POST['operation'] == "Search":
            RoleListCtl.count = 1
            self.form['pageNo'] = RoleListCtl.count
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {"form": self.form, "pageList": self.page_list})
        return res

    def get_template(self):
        return "ors/RoleList.html"

    def get_service(self):
        return RoleService()
