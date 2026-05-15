from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.RoleService import RoleService


class RoleListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["name"] = request_form.get("name", "").strip()
        self.form["description"] = request_form.get("description", "").strip()

    def display(self, request, params={}):
        RoleListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = RoleListCtl.count

        if request.POST['operation'] == "Next":
            RoleListCtl.count += 1
            self.form['page_no'] = RoleListCtl.count
        if request.POST['operation'] == "Previous":
            RoleListCtl.count -= 1
            self.form['page_no'] = RoleListCtl.count
        if request.POST['operation'] == "Search":
            RoleListCtl.count = 1
            self.form['page_no'] = RoleListCtl.count

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def get_template(self):
        return "ors/RoleList.html"

    def get_service(self):
        return RoleService()
