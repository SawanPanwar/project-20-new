from datetime import datetime
from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Faculty
from service.service.FacultyService import FacultyService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from ORS.utility.HtmlUtility import HtmlUtility


class FacultyCtl(BaseCtl):

    def preload(self, request):
        college_list = CollegeService().search({})
        course_list = CourseService().search({})
        subject_list = SubjectService().search({})
        gender_list = ["Male", "Female"]

        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "collegeId",
            int(self.form.get("college_id") or 0),
            college_list
        )
        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "courseId",
            int(self.form.get("course_id") or 0),
            course_list
        )
        self.preload_data["subject_select"] = HtmlUtility.get_list_from_beans(
            "subjectId",
            int(self.form.get("subject_id") or 0),
            subject_list
        )
        self.preload_data["gender_select"] = HtmlUtility.get_list_from_list(
            "gender",
            self.form.get("gender"),
            gender_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["first_name"] = request_form.get("firstName", "").strip()
        self.form["last_name"] = request_form.get("lastName", "").strip()
        self.form["email"] = request_form.get("email", "").strip()
        self.form["mobile_number"] = request_form.get("mobileNumber", "").strip()
        self.form["address"] = request_form.get("address", "").strip()
        self.form["gender"] = request_form.get("gender", "").strip()
        self.form["dob"] = request_form.get("dob", "").strip()
        self.form["college_id"] = request_form.get("collegeId", 0)
        self.form["course_id"] = request_form.get("courseId", 0)
        self.form["subject_id"] = request_form.get("subjectId", 0)

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))

        if pk > 0:
            obj.id = pk

        obj.first_name = self.form.get("first_name", "")
        obj.last_name = self.form.get("last_name", "")
        obj.email = self.form.get("email", "")
        obj.mobile_number = self.form.get("mobile_number", "")
        obj.address = self.form.get("address", "")
        obj.gender = self.form.get("gender", "")

        obj.dob = (
            datetime.strptime(self.form.get("dob"), "%Y-%m-%d").date()
            if self.form.get("dob")
            else None
        )

        college_id = int(self.form.get("college_id") or 0)
        obj.college_id = college_id

        college = CollegeService().get(college_id) if college_id > 0 else None
        obj.college_name = college.name if college else ""

        course_id = int(self.form.get("course_id") or 0)
        obj.course_id = course_id

        course = CourseService().get(course_id) if course_id > 0 else None
        obj.course_name = course.name if course else ""

        subject_id = int(self.form.get("subject_id") or 0)
        obj.subject_id = subject_id

        subject = SubjectService().get(subject_id) if subject_id > 0 else None
        obj.subject_name = subject.name if subject else ""

        return obj

    def model_to_form(self, obj):
        if obj is None:
            return

        self.form["id"] = obj.id
        self.form["first_name"] = obj.first_name
        self.form["last_name"] = obj.last_name
        self.form["email"] = obj.email
        self.form["mobile_number"] = obj.mobile_number
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d") if obj.dob else ""

        self.form["college_id"] = int(obj.college_id) if obj.college_id else 0
        self.form["course_id"] = int(obj.course_id) if obj.course_id else 0
        self.form["subject_id"] = int(obj.subject_id) if obj.subject_id else 0

    def input_validation(self):
        super().input_validation()

        input_error = self.form.get("input_error", {})

        if DataValidator.isNull(self.form.get("first_name")):
            input_error["first_name"] = "First Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("last_name")):
            input_error["last_name"] = "Last Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("email")):
            input_error["email"] = "Email can not be null"
            self.form["error"] = True

        elif not DataValidator.isEmail(self.form.get("email")):
            input_error["email"] = "Email must be a valid email address"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number can not be null"
            self.form["error"] = True

        elif not DataValidator.isMobileNumber(self.form.get("mobile_number")):
            input_error["mobile_number"] = "Mobile Number must be 10 digits"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("address")):
            input_error["address"] = "Address can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        faculty_id = int(params.get("id", 0))

        if faculty_id > 0:
            faculty = self.get_service().get(faculty_id)
            self.model_to_form(faculty)

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
            self.form['message'] = "Email already exist"
        else:
            faculty = self.form_to_model(Faculty())
            self.get_service().save(faculty)
            self.form['id'] = faculty.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Faculty updated successfully"
            else:
                self.form['message'] = "Faculty added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/Faculty.html"

    def get_service(self):
        return FacultyService()
