from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import Course
from service.service.CourseService import CourseService
from service.service.CollegeService import CollegeService
from ORS.utility.HtmlUtility import HtmlUtility


class CourseCtl(BaseCtl):

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
        self.form["name"] = request_form.get("name", "").strip()
        self.form["duration"] = request_form.get("duration", "").strip()
        self.form["description"] = request_form.get("description", "").strip()
        self.form["college_id"] = request_form.get("collegeId", 0)

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.name = self.form.get("name", "")
        obj.duration = self.form.get("duration", "")
        obj.description = self.form.get("description", "")

        college_id = int(self.form.get("college_id") or 0)
        obj.college_id = college_id

        college = CollegeService().get(college_id) if college_id > 0 else None
        obj.college_name = college.name if college else ""
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["duration"] = obj.duration
        self.form["description"] = obj.description
        self.form["college_id"] = int(obj.college_id) if obj.college_id else 0

    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]

        if DataValidator.isNull(self.form.get("name")):
            input_error["name"] = "Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("duration")):
            input_error["duration"] = "Duration can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("description")):
            input_error["description"] = "Description can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("college_id")) or self.form.get("college_id") == "0":
            input_error["college_id"] = "College can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):

        course_id = int(params.get("id", 0))

        if course_id > 0:
            course = self.get_service().get(course_id)
            self.model_to_form(course)

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
            self.form['message'] = "Course already exist"
        else:
            course = self.form_to_model(Course())
            self.get_service().save(course)
            self.form['id'] = course.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Course updated successfully"
            else:
                self.form['message'] = "Course added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/Course.html"

    def get_service(self):
        return CourseService()
