from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.core.paginator import Paginator

"""
It contains User business logics.   
"""


class UserService(BaseService):

    def authenticate(self, params):
        user_list = self.search(params)
        if len(user_list) > 0:
            return user_list[0]
        else:
            return None

    def search(self, params):

        page_no = int(params.get("page_no", 0))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        if page_no == 0:
            return query

        value = params.get("first_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(first_name__istartswith=value.strip())

        value = params.get("last_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(last_name__istartswith=value.strip())

        value = params.get("login", None)
        if DataValidator.isNotNull(value):
            query = query.filter(login__istartswith=value.strip())

        value = params.get("gender", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(gender__istartswith=value.strip())

        value = params.get("mobile_number", None)
        if DataValidator.isNotNull(value):
            query = query.filter(mobile_number__istartswith=value.strip())

        value = params.get("role_id", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(role_id=int(value))

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return User
