from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.MarksheetService import MarksheetService
from service.service.StudentService import StudentService
from ORS.utility.HtmlUtility import HtmlUtility


class MarksheetListCtl(BaseCtl):
    count = 1
    
    def preload(self, request):
        student_list = StudentService().search({})

        self.preload_data["student_select"] = HtmlUtility.get_list_from_beans(
            "studentId",
            int(self.form.get("student_id") or 0),
            student_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["roll_number"] = request_form.get("rollNumber", "").strip()
        self.form["name"] = request_form.get("name", "").strip()
        self.form["student_id"] = request_form.get("studentId", 0)

    def display(self, request, params={}):
        MarksheetListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = MarksheetListCtl.count

        if request.POST['operation'] == "Next":
            MarksheetListCtl.count += 1
            self.form['page_no'] = MarksheetListCtl.count
        if request.POST['operation'] == "Previous":
            MarksheetListCtl.count -= 1
            self.form['page_no'] = MarksheetListCtl.count
        if request.POST['operation'] == "Search":
            MarksheetListCtl.count = 1
            self.form['page_no'] = MarksheetListCtl.count

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/MarksheetList.html"

    def get_service(self):
        return MarksheetService()
