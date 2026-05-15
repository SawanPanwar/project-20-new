from datetime import datetime

from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import Student
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService
from ORS.utility.HtmlUtility import HtmlUtility


class StudentCtl(BaseCtl):

    def preload(self, request):
        college_list = CollegeService().search({})

        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "collegeId",
            int(self.form.get("college_id") or 0),
            college_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["first_name"] = request_form.get("firstName", "").strip()
        self.form["last_name"] = request_form.get("lastName", "").strip()
        self.form["dob"] = request_form.get("dob", "").strip()
        self.form["mobile_number"] = request_form.get("mobileNumber", "").strip()
        self.form["email"] = request_form.get("email", "").strip()
        self.form["college_id"] = request_form.get("collegeId", 0)

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))

        if pk > 0:
            obj.id = pk

        obj.first_name = self.form.get("first_name", "")
        obj.last_name = self.form.get("last_name", "")
        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )
        obj.mobile_number = self.form.get("mobile_number", "")
        obj.email = self.form.get("email", "")

        college_id = int(self.form.get("college_id") or 0)
        obj.college_id = college_id

        college = CollegeService().get(college_id) if college_id > 0 else None
        obj.college_name = college.name if college else ""

        return obj

    def model_to_form(self, obj):
        if obj is None:
            return

        self.form["id"] = obj.id
        self.form["first_name"] = obj.first_name
        self.form["last_name"] = obj.last_name
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""
        self.form["mobile_number"] = obj.mobile_number
        self.form["email"] = obj.email
        self.form["college_id"] = int(obj.college_id) if obj.college_id else 0

    def input_validation(self):

        super().input_validation()

        input_error = self.form.get("input_error", {})

        if DataValidator.isNull(self.form.get("first_name")):
            input_error["first_name"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("last_name")):
            input_error["last_name"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("dob")):
            input_error["dob"] = "Date Of Birth can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number can not be null"
            self.form["error"] = True

        elif not DataValidator.isMobileNumber(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("email")):
            input_error["email"] = "Email can not be null"
            self.form["error"] = True

        elif not DataValidator.isEmail(self.form.get("email")):
            input_error["email"] = "Email must be a valid email address"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        student_id = int(params.get("id", 0))

        if student_id > 0:
            student = self.get_service().get(student_id)
            self.model_to_form(student)

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        # Duplicate Check
        duplicate = self.get_service().get_model().objects.filter(email=self.form.get('email', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Student already exist"
        else:
            student = self.form_to_model(Student())
            self.get_service().save(student)
            self.form['id'] = student.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Student updated successfully"
            else:
                self.form['message'] = "Student added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        """Return the template path for the Student form."""
        return "ors/Student.html"

    def get_service(self):
        """Return the StudentService instance for database operations."""
        return StudentService()
