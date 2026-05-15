from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from service.models import Course
from service.service.CourseService import CourseService


class CourseCtl(BaseCtl):

    def preload(self, _request):
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["name"] = request_form.get("name", "").strip()
        self.form["description"] = request_form.get("description", "").strip()
        self.form["duration"] = request_form.get("duration", "").strip()

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.name = self.form.get("name", "")
        obj.description = self.form.get("description", "")
        obj.duration = self.form.get("duration", "")
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description
        self.form["duration"] = obj.duration

    def input_validation(self):
        super().input_validation()

        input_error = self.form["input_error"]

        if DataValidator.isNull(self.form.get("name")):
            input_error["name"] = "Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("description")):
            input_error["description"] = "Description can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("duration")):
            input_error["duration"] = "Duration can not be null"
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

        # Duplicate Check
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
        """Return the template path for the Course form."""
        return "ors/Course.html"

    def get_service(self):
        """Return the CourseService instance for database operations."""
        return CourseService()