import os
import uuid
from datetime import datetime
from django.conf import settings
from django.db.models.manager import BaseManager
from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Role, User
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from ORS.utility.HtmlUtility import HtmlUtility
from ORS.utility.FileUtility import FileUtility


class UserCtl(BaseCtl):
    """Controller for managing User CRUD operations."""

    def preload(self, request):
        """Load role list for the role dropdown before rendering the form."""
        role_list: BaseManager[Role] = RoleService().search(self.form)
        gender_list = ["Male", "Female"]
        self.preload_data["role_list"] = role_list
        self.preload_data["gender_list"] = gender_list

        self.preload_data["role_select"] = HtmlUtility.get_list_from_beans(
            "roleId",
            int(self.form.get("roleId") or 0),
            self.preload_data["role_list"],
        )
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender", self.form.get("gender"), self.preload_data["gender_list"]
        )
        print("a-------", self.form.get("gender"))
        return self.preload_data

    def request_to_form(self, requestForm):
        """Populate form dictionary from HTTP POST request data."""
        self.form["id"] = requestForm.get("id", 0)
        self.form["firstName"] = requestForm.get("firstName", "")
        self.form["lastName"] = requestForm.get("lastName", "")
        self.form["login"] = requestForm.get("login", "")
        self.form["password"] = requestForm.get("password", "")
        self.form["dob"] = requestForm.get("dob", "")
        self.form["mobileNumber"] = requestForm.get("mobileNumber", "")
        self.form["gender"] = requestForm.get("gender", "")
        self.form["roleId"] = requestForm.get("roleId", 0)

    def form_to_model(self, obj):
        """Populate a User model instance from the form dictionary and return it."""
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.first_name = self.form.get("firstName", "")
        obj.last_name = self.form.get("lastName", "")
        obj.login = self.form.get("login", "")
        obj.password = self.form.get("password", "")
        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        obj.mobile_number = self.form.get("mobileNumber", "")
        obj.gender = self.form.get("gender", "")
        obj.role_id = int(self.form.get("roleId") or 0)
        if int(self.form['roleId']) > 0:
            role = RoleService().get(int(self.form['roleId']))
            obj.role_name = role.name
        obj.photo = self.form.get("photo", "")
        return obj

    def model_to_form(self, obj):
        """Populate form dictionary from a User model instance."""
        if obj == None:
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.first_name
        self.form["lastName"] = obj.last_name
        self.form["login"] = obj.login
        self.form["password"] = obj.password
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["mobileNumber"] = obj.mobile_number
        self.form["gender"] = obj.gender
        self.form["roleId"] = int(obj.role_id) if obj.role_id else 0
        self.form["photo"] = obj.photo or ""



    def input_validation(self):
        """Validate required fields and populate inputError messages. Returns True if any error exists."""
        super().input_validation()
        inputError = self.form.get("inputError", {})
        if DataValidator.isNull(self.form.get("firstName")):
            inputError["firstName"] = "First Name can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("lastName")):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("login")):
            inputError["login"] = "Login can not be null"
            self.form["error"] = True
        else:
            if not DataValidator.isEmail(self.form.get("login")):
                inputError["login"] = "Login must be a valid email address"
                self.form["error"] = True
            else:
                current_id = int(self.form.get("id") or 0)
                duplicate = User.objects.filter(login=self.form.get("login")).exclude(id=current_id).exists()
                if duplicate:
                    inputError["login"] = "This email is already registered"
                    self.form["error"] = True

        if DataValidator.isNull(self.form.get("password")):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form.get("mobileNumber")):
            inputError["mobileNumber"] = "Mobile Number can not be null"
            self.form["error"] = True
        else:
            if not DataValidator.isMobileNumber(self.form.get("mobileNumber")):
                inputError["mobileNumber"] = "Mobile Number must be 10 digits"
                self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        """Render the User form. Loads existing user data if a valid id is provided in params."""
        if params["id"] > 0:
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
            # self.preload(request);
        res = render(
            request,
            self.get_template(),
            {"form": self.form, "preload_data": self.preload(request)},
        )
        return res

    def submit(self, request, params={}):
        current_id = int(self.form.get("id", 0))
        photo_file = request.FILES.get("photo")

        try:
            if photo_file:
                # Extract extension
                self.form["photo"] = FileUtility.upload_photo(photo_file)

            elif current_id > 0:
                # Keep old photo during update
                try:
                    existing_user = User.objects.get(id=current_id)
                    self.form["photo"] = existing_user.photo or ""
                except User.DoesNotExist:
                    self.form["photo"] = ""
            else:
                self.form["photo"] = ""

            pk = int(self.form.get('id', 0))

            # Duplicate Check
            duplicate = self.get_service().get_model().objects.filter(login=self.form.get('login', ''))

            if pk > 0:
                duplicate = duplicate.exclude(id=pk)

            if duplicate.exists():
                self.form['error'] = True
                self.form['message'] = "Login ID already exist"
            else:
                user = self.form_to_model(User())
                self.get_service().save(user)
                self.form['id'] = user.id
                self.form['error'] = False

                if pk > 0:
                    self.form['message'] = "User updated successfully"
                else:
                    self.form['message'] = "User added successfully..!!"
        except Exception as e:
            self.form["error"] = True
            self.form["message"] = str(e)

        return render(
            request, self.get_template(), {
                'form': self.form,
                'preload_data': self.preload(request)
            })

    def get_template(self):
        """Return the template path for the User form."""
        return "ors/User.html"

    def get_service(self):
        """Return the UserService instance for database operations."""
        return UserService()
