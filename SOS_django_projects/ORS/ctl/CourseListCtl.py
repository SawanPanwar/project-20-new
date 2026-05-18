from django.shortcuts import render, redirect
from .BaseCtl import BaseCtl
from service.models import Course
from service.service.CourseService import CourseService


class CourseListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["name"] = request_form.get("name", "").strip()
        self.form["duration"] = request_form.get("duration", "").strip()
        self.form["description"] = request_form.get("description", "").strip()

    def display(self, request, params={}):
        CourseListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = CourseListCtl.count

        if request.POST['operation'] == "Next":
            CourseListCtl.count += 1
            self.form['page_no'] = CourseListCtl.count
        if request.POST['operation'] == "Previous":
            CourseListCtl.count -= 1
            self.form['page_no'] = CourseListCtl.count
        if request.POST['operation'] == "Search":
            CourseListCtl.count = 1
            self.form['page_no'] = CourseListCtl.count

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def get_template(self):
        return "ors/CourseList.html"

    def get_service(self):
        return CourseService()
