from .BaseCtl import BaseCtl
from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from service.models import Subject
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService
from ORS.utility.HtmlUtility import HtmlUtility


class SubjectCtl(BaseCtl):

    def preload(self, request):
        course_list = CourseService().search({})

        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "courseId",
            int(self.form.get("course_id") or 0),
            course_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["name"] = request_form.get("name", "").strip()
        self.form["description"] = request_form.get("description", "").strip()
        self.form["course_id"] = request_form.get("courseId", 0)

    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.name = self.form.get("name", "").strip()
        obj.description = self.form.get("description", "").strip()

        course_id = int(self.form.get("course_id") or 0)
        obj.course_id = course_id

        course = CourseService().get(course_id) if course_id > 0 else None
        obj.course_name = course.name if course else ""

        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description
        self.form["course_id"] = int(obj.course_id) if obj.course_id else 0

    def input_validation(self):

        super().input_validation()

        input_error = self.form["input_error"]

        if DataValidator.isNull(self.form["name"]):
            input_error["name"] = "Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form["description"]):
            input_error["description"] = "Description can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):

        subject_id = int(params.get("id", 0))

        if subject_id > 0:
            subject = self.get_service().get(subject_id)
            self.model_to_form(subject)

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
            self.form['message'] = "Subject already exist"
        else:
            subject = self.form_to_model(Subject())
            self.get_service().save(subject)
            self.form['id'] = subject.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Subject updated successfully"
            else:
                self.form['message'] = "Subject added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/Subject.html"

    def get_service(self):
        return SubjectService()
