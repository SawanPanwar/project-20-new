from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService
from ORS.utility.HtmlUtility import HtmlUtility


class SubjectListCtl(BaseCtl):
    count = 1

    def preload(self, request):
        course_list = CourseService().search({})

        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "courseId",
            int(self.form.get("course_id") or 0),
            course_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["name"] = request_form.get("name", "").strip()
        self.form["description"] = request_form.get("description", "").strip()
        self.form["course_id"] = request_form.get("courseId", 0)

    def display(self, request, params={}):
        SubjectListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = SubjectListCtl.count

        if request.POST['operation'] == "Next":
            SubjectListCtl.count += 1
            self.form['page_no'] = SubjectListCtl.count
        if request.POST['operation'] == "Previous":
            SubjectListCtl.count -= 1
            self.form['page_no'] = SubjectListCtl.count
        if request.POST['operation'] == "Search":
            SubjectListCtl.count = 1
            self.form['page_no'] = SubjectListCtl.count

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/SubjectList.html"

    def get_service(self):
        return SubjectService()
