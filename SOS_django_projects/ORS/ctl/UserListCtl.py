from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from ORS.utility.HtmlUtility import HtmlUtility
from django.db.models.manager import BaseManager
from service.models import Role


class UserListCtl(BaseCtl):
    count = 1

    def preload(self, request):

        role_list = RoleService().search({})
        gender_list = ["Male", "Female"]

        self.preload_data["role_select"] = HtmlUtility.get_list_from_beans(
            "roleId",
            int(self.form.get("role_id") or 0),
            role_list
        )
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender",
            self.form.get("gender"),
            gender_list
        )
        return self.preload_data

    def request_to_form(self, request_form):

        self.form["first_name"] = request_form.get("firstName", None)
        self.form["last_name"] = request_form.get("lastName", None)
        self.form["login"] = request_form.get("login", None)
        self.form["mobile_number"] = request_form.get("mobileNumber", None)
        self.form["gender"] = request_form.get("gender", None)
        self.form["role_id"] = request_form.get("roleId", None)

    def display(self, request, params={}):

        UserListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = UserListCtl.count

        if request.POST['operation'] == "Next":
            UserListCtl.count += 1
            self.form['page_no'] = UserListCtl.count

        if request.POST['operation'] == "Previous":
            UserListCtl.count -= 1
            self.form['page_no'] = UserListCtl.count

        if request.POST['operation'] == "Search":
            UserListCtl.count = 1
            self.form['page_no'] = UserListCtl.count

        self.page_list = self.get_service().search(self.form)

        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/UserList.html"

    def get_service(self):
        return UserService()
