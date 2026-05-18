from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import College
from service.service.CollegeService import CollegeService


class CollegeListCtl(BaseCtl):
    count = 1

    def request_to_form(self, request_form):
        self.form["name"] = request_form.get("name", "").strip()
        self.form["address"] = request_form.get("address", "").strip()
        self.form["city"] = request_form.get("city", "").strip()
        self.form["state"] = request_form.get("state", "").strip()
        self.form["phone_number"] = request_form.get("phoneNumber", "").strip()

    def display(self, request, params={}):
        CollegeListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = CollegeListCtl.count

        if request.POST['operation'] == "Next":
            CollegeListCtl.count += 1
            self.form['page_no'] = CollegeListCtl.count
        if request.POST['operation'] == "Previous":
            CollegeListCtl.count -= 1
            self.form['page_no'] = CollegeListCtl.count
        if request.POST['operation'] == "Search":
            CollegeListCtl.count = 1
            self.form['page_no'] = CollegeListCtl.count

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def get_template(self):
        return "ors/CollegeList.html"

    def get_service(self):
        return CollegeService()
