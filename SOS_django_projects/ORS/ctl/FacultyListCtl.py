from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.FacultyService import FacultyService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from ORS.utility.HtmlUtility import HtmlUtility


class FacultyListCtl(BaseCtl):
    count = 1

    def preload(self, request):
        college_list = CollegeService().search({})
        course_list = CourseService().search({})
        subject_list = SubjectService().search({})

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
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["first_name"] = requestForm.get("firstName", "").strip()
        self.form["last_name"] = requestForm.get("lastName", "").strip()
        self.form["email"] = requestForm.get("email", "").strip()
        self.form["college_id"] = requestForm.get("collegeId", 0)
        self.form["course_id"] = requestForm.get("courseId", 0)
        self.form["subject_id"] = requestForm.get("subjectId", 0)

    def display(self, request, params={}):
        FacultyListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = FacultyListCtl.count

        if request.POST['operation'] == "Next":
            FacultyListCtl.count += 1
            self.form['page_no'] = FacultyListCtl.count
        if request.POST['operation'] == "Previous":
            FacultyListCtl.count -= 1
            self.form['page_no'] = FacultyListCtl.count
        if request.POST['operation'] == "Search":
            FacultyListCtl.count = 1
            self.form['page_no'] = FacultyListCtl.count

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/FacultyList.html"

    def get_service(self):
        return FacultyService()
