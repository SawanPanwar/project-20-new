from service.models import Faculty
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.core.paginator import Paginator


class FacultyService(BaseService):

    def search(self, params):

        page_no = int(params.get("page_no", 1))
        page_size = self.pageSize

        query = self.get_model().objects.all()

        value = params.get("first_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(first_name__istartswith=value.strip())

        value = params.get("last_name", None)
        if DataValidator.isNotNull(value):
            query = query.filter(last_name__istartswith=value.strip())

        value = params.get("email", None)
        if DataValidator.isNotNull(value):
            query = query.filter(email__istartswith=value.strip())

        value = params.get("college_id", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(college_id=value)

        value = params.get("course_id", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(course_id=value)

        value = params.get("subject_id", None)
        if DataValidator.isNotNull(value) and str(value) != "0":
            query = query.filter(subject_id=value)

        paginator = Paginator(query, page_size)

        page_obj = paginator.get_page(page_no)

        params["has_next"] = page_obj.has_next()
        params["has_previous"] = page_obj.has_previous()
        params["start_index"] = (page_no - 1) * page_size

        return page_obj

    def get_model(self):
        return Faculty
