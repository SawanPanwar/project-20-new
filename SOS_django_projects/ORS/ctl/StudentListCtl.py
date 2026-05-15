from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService
from ORS.utility.HtmlUtility import HtmlUtility


class StudentListCtl(BaseCtl):

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
        self.form["email"] = request_form.get("email", "").strip()
        self.form["college_id"] = request_form.get("collegeId", 0)

    def display(self, request, params={}):
        StudentListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = StudentListCtl.count

        if request.POST['operation'] == "Next":
            StudentListCtl.count += 1
            self.form['page_no'] = StudentListCtl.count
        if request.POST['operation'] == "Previous":
            StudentListCtl.count -= 1
            self.form['page_no'] = StudentListCtl.count
        if request.POST['operation'] == "Search":
            StudentListCtl.count = 1
            self.form['page_no'] = StudentListCtl.count

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/StudentList.html"

    def get_service(self):
        return StudentService()
