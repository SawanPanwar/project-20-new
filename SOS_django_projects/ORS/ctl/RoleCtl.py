from .BaseCtl import BaseCtl
from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from service.models import Role
from service.service.RoleService import RoleService


class RoleCtl(BaseCtl):

    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", 0)
        self.form["name"] = requestForm.get("name", "")
        self.form["description"] = requestForm.get("description", "")

    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form.get("id", 0))
        if pk > 0:
            obj.id = pk
        obj.name = self.form.get("name", "")
        obj.description = self.form.get("description", "")
        return obj

    # Populate Form from Model
    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description

    def preload(self, _request):
        """Load preload data required by the Role page before rendering."""
        return self.preload_data

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if DataValidator.isNull(self.form["name"]):
            inputError["name"] = "Name can not be null"
            self.form["error"] = True
        if DataValidator.isNull(self.form["description"]):
            inputError["description"] = "Description can not be null"
            self.form["error"] = True
        return self.form["error"]

    # Display Role page
    def display(self, request, params={}):

        role_id = int(params.get("id", 0))

        if role_id > 0:
            role = self.get_service().get(role_id)
            self.model_to_form(role)

        return render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request),
        })

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        # Duplicate Check
        duplicate = self.get_service().get_model().objects.filter(name=self.form.get('name', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "Role already exist"
        else:
            role = self.form_to_model(Role())
            self.get_service().save(role)
            self.form['id'] = role.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "Role updated successfully"
            else:
                self.form['message'] = "Role added successfully..!!"

        return render(
            request, self.get_template(), {
                'form': self.form,
                'preload_data': self.preload(request)
            })

    # Template html of Role page
    def get_template(self):
        return "ors/Role.html"

    # Service of Role
    def get_service(self):
        return RoleService()
