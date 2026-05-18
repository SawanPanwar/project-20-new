from datetime import datetime
from django.db.models.manager import BaseManager
from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Role, User
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from ORS.utility.HtmlUtility import HtmlUtility
from ORS.utility.FileUtility import FileUtility


class UserCtl(BaseCtl):

    def preload(self, request):

        role_list = RoleService().search({})
        gender_list = ["Male", "Female"]

        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender",
            self.form.get("gender"),
            gender_list
        )

        self.preload_data["role_select"] = HtmlUtility.get_list_from_beans(
            "roleId",
            int(self.form.get("role_id") or 0),
            role_list
        )

        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["first_name"] = request_form.get("firstName", "").strip()
        self.form["last_name"] = request_form.get("lastName", "").strip()
        self.form["login"] = request_form.get("login", "").strip()
        self.form["password"] = request_form.get("password", "").strip()
        self.form["dob"] = request_form.get("dob", "").strip()
        self.form["gender"] = request_form.get("gender", "").strip()
        self.form["mobile_number"] = request_form.get("mobileNumber", "").strip()
        self.form["role_id"] = request_form.get("roleId", 0)

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.first_name = self.form.get("first_name", "")
        obj.last_name = self.form.get("last_name", "")
        obj.login = self.form.get("login", "")
        obj.password = self.form.get("password", "")

        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )

        obj.gender = self.form.get("gender", "")
        obj.mobile_number = self.form.get("mobile_number", "")

        role_id = int(self.form.get("role_id") or 0)
        obj.role_id = role_id

        role = RoleService().get(role_id) if role_id > 0 else None
        obj.role_name = role.name if role else ""

        obj.photo = self.form.get("photo", "")

        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["first_name"] = obj.first_name
        self.form["last_name"] = obj.last_name
        self.form["login"] = obj.login
        self.form["password"] = obj.password
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["gender"] = obj.gender
        self.form["mobile_number"] = obj.mobile_number
        self.form["role_id"] = int(obj.role_id) if obj.role_id else 0
        self.form["photo"] = obj.photo or ""

    def input_validation(self):

        super().input_validation()

        input_error = self.form.get("input_error", {})

        if DataValidator.isNull(self.form.get("first_name")):
            input_error["first_name"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("last_name")):
            input_error["last_name"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("login")):
            input_error["login"] = "Login can not be null"
            self.form["error"] = True

        elif not DataValidator.isEmail(self.form.get("login")):
            input_error["login"] = "Login must be a valid email address"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("password")):
            input_error["password"] = "Password can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("dob")):
            input_error["dob"] = "DOB can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("gender")) or self.form.get("gender") == "0":
            input_error["gender"] = "Gender can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number can not be null"
            self.form["error"] = True

        elif not DataValidator.isMobileNumber(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("role_id")) or self.form.get("role_id") == "0":
            input_error["role_id"] = "Role can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        user_id = int(params.get("id", 0))

        if user_id > 0:
            user = self.get_service().get(user_id)
            self.model_to_form(user)

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        duplicate = self.get_service().get_model().objects.filter(login=self.form.get('login', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Login ID already exist"
        else:
            photo_file = request.FILES.get("photo")

            if photo_file:
                self.form["photo"] = FileUtility.upload_photo(photo_file)
            elif pk > 0:
                existing_user = self.get_service().get(pk)
                self.form["photo"] = existing_user.photo or ""
            else:
                self.form["photo"] = ""

            user = self.form_to_model(User())
            self.get_service().save(user)

            self.form['id'] = user.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "User updated successfully"
            else:
                self.form['message'] = "User added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/User.html"

    def get_service(self):
        return UserService()
