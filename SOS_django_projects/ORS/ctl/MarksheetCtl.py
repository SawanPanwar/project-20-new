from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Marksheet
from service.service.MarksheetService import MarksheetService
from service.service.StudentService import StudentService
from ORS.utility.HtmlUtility import HtmlUtility


class MarksheetCtl(BaseCtl):

    def preload(self, request):
        student_list = StudentService().search({})

        self.preload_data["student_select"] = HtmlUtility.get_list_from_beans(
            "studentId",
            int(self.form.get("student_id") or 0),
            student_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["roll_number"] = request_form.get("rollNumber", "").strip()
        self.form["student_id"] = request_form.get("studentId", 0)
        self.form["name"] = request_form.get("name", "").strip()
        self.form["year"] = request_form.get("year", "").strip()
        self.form["physics"] = request_form.get("physics", "").strip()
        self.form["chemistry"] = request_form.get("chemistry", "").strip()
        self.form["maths"] = request_form.get("maths", "").strip()

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.roll_number = self.form.get("roll_number", "")

        student_id = int(self.form.get("student_id") or 0)
        obj.student_id = student_id

        student = StudentService().get(student_id) if student_id > 0 else None
        obj.name = student.first_name + ' ' + student.last_name if student else ""

        obj.year = int(self.form.get("year") or 0)
        obj.physics = int(float(self.form.get("physics") or 0))
        obj.chemistry = int(float(self.form.get("chemistry") or 0))
        obj.maths = int(float(self.form.get("maths") or 0))

        return obj

    def model_to_form(self, obj):
        if obj is None:
            return

        self.form["id"] = obj.id
        self.form["roll_number"] = obj.roll_number
        self.form["student_id"] = int(obj.student_id) if obj.student_id else 0
        self.form["year"] = obj.year
        self.form["physics"] = obj.physics
        self.form["chemistry"] = obj.chemistry
        self.form["maths"] = obj.maths
        self.form["total"] = obj.total
        self.form["percentage"] = obj.percentage

    def input_validation(self):
        super().input_validation()
        input_error = self.form["input_error"]

        if DataValidator.isNull(self.form.get("roll_number")):
            input_error["roll_number"] = "Roll Number can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("student_id")) or self.form.get("student_id") == "0":
            input_error["student_id"] = "Student can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("physics")):
            input_error["physics"] = "Physics can not be null"
            self.form["error"] = True
        elif not DataValidator.isRange(self.form.get("physics"), 0, 100):
            input_error["physics"] = "Physics must be between 0 and 100"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("chemistry")):
            input_error["chemistry"] = "Chemistry can not be null"
            self.form["error"] = True
        elif not DataValidator.isRange(self.form.get("chemistry"), 0, 100):
            input_error["chemistry"] = "Chemistry must be between 0 and 100"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("maths")):
            input_error["maths"] = "Maths can not be null"
            self.form["error"] = True
        elif not DataValidator.isRange(self.form.get("maths"), 0, 100):
            input_error["maths"] = "Maths must be between 0 and 100"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("year")):
            input_error["year"] = "Year can not be null"
            self.form["error"] = True
        elif not DataValidator.isInteger(self.form.get("year")):
            input_error["year"] = "Year must be an integer"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        marksheet_id = int(params.get("id", 0))

        if marksheet_id > 0:
            marksheet = self.get_service().get(marksheet_id)
            self.model_to_form(marksheet)

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        # Duplicate Check
        duplicate = self.get_service().get_model().objects.filter(roll_number=self.form.get('roll_number', 0))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Roll No already exist"
        else:
            marksheet = self.form_to_model(Marksheet())
            self.get_service().save(marksheet)
            self.form['id'] = marksheet.id
            self.form["total"] = marksheet.total
            self.form["percentage"] = marksheet.percentage
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
        """Return the template path for the Marksheet form."""
        return "ors/Marksheet.html"

    def get_service(self):
        """Return the MarksheetService instance for database operations."""
        return MarksheetService()
