from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import College
from service.service.CollegeService import CollegeService


class CollegeCtl(BaseCtl):

    def preload(self, request):
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["name"] = request_form.get("name", "").strip()
        self.form["address"] = request_form.get("address", "").strip()
        self.form["city"] = request_form.get("city", "").strip()
        self.form["state"] = request_form.get("state", "").strip()
        self.form["phone_number"] = request_form.get("phoneNumber", "").strip()

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.name = self.form.get("name", "")
        obj.address = self.form.get("address", "")
        obj.city = self.form.get("city", "")
        obj.state = self.form.get("state", "")
        obj.phone_number = self.form.get("phone_number", "")
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["address"] = obj.address
        self.form["city"] = obj.city
        self.form["state"] = obj.state
        self.form["phone_number"] = obj.phone_number

    def input_validation(self):
        super().input_validation()
        input_error = self.form.get("input_error", {})

        if DataValidator.isNull(self.form.get("name")):
            input_error["name"] = "Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("address")):
            input_error["address"] = "Address can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("city")):
            input_error["city"] = "City can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("state")):
            input_error["state"] = "State can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("phone_number")):
            input_error["phone_number"] = "Phone Number can not be null"
            self.form["error"] = True
        elif not DataValidator.isMobileNumber(self.form.get("phone_number")):
            input_error["phone_number"] = "Phone Number must be a mobile number (10 digits)"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        college_id = int(params.get("id", 0))

        if college_id > 0:
            college = self.get_service().get(college_id)
            self.model_to_form(college)

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        duplicate = self.get_service().get_model().objects.filter(name=self.form.get('name', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "College already exist"
        else:
            college = self.form_to_model(College())
            self.get_service().save(college)
            self.form['id'] = college.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "College updated successfully"
            else:
                self.form['message'] = "College added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/College.html"

    def get_service(self):
        return CollegeService()
