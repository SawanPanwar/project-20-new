import re

from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from service.service.UserService import UserService


class LoginCtl(BaseCtl):

    def request_to_form(self, requestFrom):
        self.form["loginId"] = requestFrom["loginId"]
        self.form["password"] = requestFrom["password"]
        self.form["rememberMe"] = requestFrom.get("rememberMe", False)

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["loginId"])):
            inputError["loginId"] = "Login can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        # if request.session.get("loginId"):
        #     return redirect('/ORS/Welcome')
        return render(request, self.get_template(), {"form": self.form})

    def submit(self, request, params={}):
        user = self.get_service().authenticate(self.form)
        if (user is None):
            self.form["error"] = True
            self.form["message"] = "Invalid Login or Password"
            res = render(request, self.get_template(), {"form": self.form})
        else:
            if self.form.get("rememberMe"):
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
            else:
                request.session.set_expiry(0)  # expires when browser closes
            request.session["userId"] = user.id
            request.session["loginId"] = user.login
            request.session["firstName"] = user.first_name
            request.session["lastName"] = user.last_name
            res = redirect('/ORS/Welcome')
        return res

    # Template html of Role page    
    def get_template(self):
        return "ors/Login.html"

        # Service of Role

    def get_service(self):
        return UserService()
